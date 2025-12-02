from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Entry, Tag
from .serializers import EntrySerializer, TagSerializer


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Дозвольте редагувати тільки авторам запису"""
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class EntryViewSet(viewsets.ModelViewSet):
    serializer_class = EntrySerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'tags__name']
    ordering_fields = ['created']
    ordering = ['-created']

    def get_queryset(self):
        """Кожен користувач бачить тільки свої записи"""
        return Entry.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        """Автоматично встановлюємо автора запису"""
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'])
    def by_tag(self, request):
        """API endpoint для отримання записів за тегом"""
        tag_name = request.query_params.get('name')
        if tag_name:
            entries = self.get_queryset().filter(tags__name=tag_name)
            serializer = self.get_serializer(entries, many=True)
            return Response(serializer.data)
        return Response({'error': 'Tag name required'}, status=400)

    @action(detail=True, methods=['get'])
    def similar(self, request, pk=None):
        """Отримати схожі записи за тегами"""
        entry = self.get_object()
        similar_entries = Entry.objects.filter(
            tags__in=entry.tags.all(),
            author=request.user
        ).exclude(id=entry.id).distinct()
        serializer = self.get_serializer(similar_entries, many=True)
        return Response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]