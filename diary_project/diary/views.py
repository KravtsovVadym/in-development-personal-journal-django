from rest_framework import viewsets, permissions, filters 
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Tag, Entry
from .serializers import TagSerializer, EntrySerializer

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class EntryViewSet(viewsets.ModelViewSet):
    serializer_class = EntrySerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content","tags__name"]
    ordering_fields = ["created"]
    ordering = ["-created"]


    def get_queryset(self):
        """Return only the entries that belong to the current authenticated user"""
        return Entry.objects.filter(author=self.request.user)