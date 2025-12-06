from rest_framework import serializers
from .models import Tag, Entry
from django.contrib.auth import get_user_model

User = get_user_model()

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]

class EntrySerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,  
        write_only=True,
        source="tags"
    )
    author_username = serializers.CharField(
        source="author.username",
        read_only=True
        )

    class Meta:
        model = Entry
        fields = [
            "id",
            "title",
            "tags",
            "tag_ids",
            "content",
            "created",
            "updated",
            "author_username",
            ]
        read_only_fields = [
            "id",
            "created",
            "updated",
            "author_username"
        ]

    def create(self, validate_data):
        tags = validate_data.pop("tags", [])
        entry = Entry.objects.create(**validate_data)
        entry.tags.set(tags)
        return entry
    
    def update(self, instance, validate_data):
        tags = validate_data.pop("tags", None)
        for attr, val in validate_data.items():
            setattr(instance, attr, val )
        instance.save()
        if tags is not None:
            instance.tags.set(tags)
        return instance
    