from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Entry(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', related_name='entries', blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created']
        verbose_name = 'record'
        verbose_name_plural = 'records'

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'tag'
        verbose_name_plural = 'tags'