from django.test import TestCase
from diary.models import Entry, Tag
from django.contrib.auth import get_user_model

User = get_user_model()

class EntryTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="Donald")
    
    def test_cascade_delete(self):
        Entry.objects.create(
            author=self.user,
            title="test",
            content="Hello, this is a test for the Entry model"
            )
        self.user.delete()
        self.assertEqual(Entry.objects.count(), 0)
    
    
    def test_tags(self):
        entry = Entry.objects.create(
            author=self.user,
            title="test",
            content="Hello, it's me, now we check the tag table"
            )
        tag = Tag.objects.create(name="My first tag")
        entry.tags.add(tag)
        self.assertEqual(entry.tags.count(), 1)
        self.assertIn(entry, tag.entries.all()) # type: ignore


