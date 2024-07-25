from django.test import TestCase
from django.contrib.auth.models import User
from homelessness_advice.models import Post, PostImage

class PostModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user', password='password')
        cls.post = Post.objects.create(
            title='Test Title',
            slug='test-title',
            author=cls.user,
            content='Test content',
            status='published'
        )

    def test_post_str_method(self):
        self.assertEqual(str(self.post), 'Test Title')

    def test_post_image_str_method(self):
        post_image = PostImage.objects.create(
            post=self.post,
            image='sample-image.jpg'
        )
        self.assertEqual(str(post_image), 'Image for Test Title')

    def test_post_default_status(self):
        post = Post.objects.create(
            title='Another Test Title',
            slug='another-test-title',
            author=self.user,
            content='Another test content'
        )
        self.assertEqual(post.status, 'draft')
