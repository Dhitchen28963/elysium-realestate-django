from django.test import TestCase
from faq.models import FAQ, Comment
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

class FAQModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_string_representation(self):
        faq = FAQ(title='Test FAQ', author=self.user, content='Test content', status='published')
        self.assertEqual(str(faq), faq.title)

    def test_create_faq(self):
        faq = FAQ.objects.create(title='Test FAQ', author=self.user, content='Test content', status='published')
        self.assertEqual(faq.title, 'Test FAQ')
        self.assertEqual(faq.author.username, 'testuser')
        self.assertEqual(faq.content, 'Test content')
        self.assertEqual(faq.status, 'published')

class CommentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.faq = FAQ.objects.create(title='Test FAQ', author=self.user, content='Test content', status='published')

    def test_string_representation(self):
        comment = Comment(post=self.faq, author=self.user, body='Test comment')
        self.assertEqual(str(comment), f'Comment by {self.user.username} on {self.faq.title}')

    def test_create_comment(self):
        comment = Comment.objects.create(post=self.faq, author=self.user, body='Test comment')
        self.assertEqual(comment.post.title, 'Test FAQ')
        self.assertEqual(comment.author.username, 'testuser')
        self.assertEqual(comment.body, 'Test comment')

    def test_comment_content_type(self):
        content_type = ContentType.objects.get_for_model(FAQ)
        comment = Comment.objects.create(post=self.faq, author=self.user, body='Test comment', content_type=content_type, object_id=self.faq.id)
        self.assertEqual(comment.content_type, content_type)
        self.assertEqual(comment.object_id, self.faq.id)
