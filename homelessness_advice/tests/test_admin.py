from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from homelessness_advice.models import Post, PostImage

class PostAdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser(username='admin', password='admin')
        cls.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=cls.user,
            content='Test content',
            status='published'
        )
        cls.post_image = PostImage.objects.create(
            post=cls.post,
            image='sample-image.jpg'
        )

    def test_post_admin_change_view(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin:homelessness_advice_post_change', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_post_admin_list_view(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin:homelessness_advice_post_changelist'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_post_image_inline(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin:homelessness_advice_post_change', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'sample-image.jpg')
