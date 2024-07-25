from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from faq.models import FAQ, Comment, FAQImage

class FAQModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_create_faq(self):
        faq = FAQ.objects.create(
            title='Test FAQ',
            author=self.user,
            content='This is a test FAQ.',
            status='draft'
        )
        self.assertEqual(faq.title, 'Test FAQ')
        self.assertEqual(faq.author.username, 'testuser')
        self.assertEqual(faq.status, 'draft')
        self.assertEqual(str(faq), 'Test FAQ')


class CommentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.faq = FAQ.objects.create(
            title='Test FAQ',
            author=self.user,
            content='This is a test FAQ.',
            status='published'
        )

    def test_create_comment(self):
        comment = Comment.objects.create(
            post=self.faq,
            author=self.user,
            body='This is a test comment.',
            approved=True,
            content_type=ContentType.objects.get_for_model(FAQ),
            object_id=self.faq.id,
        )
        self.assertEqual(comment.post.title, 'Test FAQ')
        self.assertEqual(comment.author.username, 'testuser')
        self.assertEqual(comment.body, 'This is a test comment.')
        self.assertTrue(comment.approved)
        self.assertEqual(str(comment), f'Comment by testuser on Test FAQ')


class FAQImageModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.faq = FAQ.objects.create(
            title='Test FAQ',
            author=self.user,
            content='This is a test FAQ.',
            status='published'
        )

    def test_create_faq_image(self):
        faq_image = FAQImage.objects.create(
            faq=self.faq,
            image='test_image.jpg'
        )
        self.assertEqual(faq_image.faq.title, 'Test FAQ')
        self.assertEqual(faq_image.image, 'test_image.jpg')
        self.assertEqual(str(faq_image), 'Image for Test FAQ')
