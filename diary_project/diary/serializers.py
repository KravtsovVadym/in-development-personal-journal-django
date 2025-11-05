from rest_framework import serializers
from diary.models import Entry, Tag
from django.contrib.auth import get_user_model

User = get_user_model()  


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        field = ['id', 'name']

class EntrySerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    pass