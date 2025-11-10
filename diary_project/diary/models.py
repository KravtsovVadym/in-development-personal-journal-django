from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Tag name",
        unique=True,
        db_index=True,
    )
    class Meta:
        ordering = ["name"]
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name

class Entry(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_index=True,
        null=False,
        blank=False,
        related_name="journal_entries",
        verbose_name="Author",
        help_text="Name of the author"
    )
    title = models.CharField(
        verbose_name="Title",
        max_length=200,
        blank=False,
        null=False,
        help_text="Enter the main content text"
    )
    content = models.TextField(
        verbose_name="Content",
        max_length=500,
        blank=False,
        null=False,
        help_text="Enter content"
    )
    created_at = models.DateTimeField(
        verbose_name="Created",
        db_index=True,
        auto_now_add=True,
        help_text="Date of creation"
    )
    updated_at = models.DateTimeField(
        verbose_name="Updated",
        auto_now=True,
        help_text="Date update"
    )
    tags = models.ManyToManyField(Tag,
        verbose_name="Tag",
        blank=True,
        related_name="entries",
        help_text="Select a tag for this entry"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Entry"
        verbose_name_plural = "Entries"
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["author", "-created_at"])
        ]

    def __str__(self):
        return self.title