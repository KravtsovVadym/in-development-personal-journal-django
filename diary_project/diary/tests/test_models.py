from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from diary.models import Entry, Tag

User = get_user_model()

class EntryCaseTest(TestCase):

        
    '''Creates a new object each time for each test'''
    def setUp(self):
        self.author = User.objects.create_user(username="Vadim")

    def test_case_delete(self):
        Entry.objects.create(
            author=self.author,
            title="test header",
            content="Here is the content for Django tests"
            )
        self.author.delete()
        self.assertEqual(Entry.objects.count(), 0)

    def test_case_many_to_many(self):
        self.entry = Entry.objects.create(
            author=self.author,
            title="test header",
            content="Here is the content for Django tests")
        tag = Tag.objects.create(name="Developers")
        self.entry.tags.add(tag)
        self.assertEqual(self.entry.tags.count(), 1)
        self.assertIn(self.entry, tag.entries.all())
    
    def test_case_unniquess(self):
        '''We check the Tag model for uniqueness'''
        with self.assertRaises(IntegrityError):
            tag1 = Tag.objects.create(name="Developers")
            tag2 = Tag.objects.create(name="Developers")
