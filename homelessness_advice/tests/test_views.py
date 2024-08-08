from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from homelessness_advice.models import Homeless

class HomelessViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user', password='password')
        cls.homeless = Homeless.objects.create(
            title='Test Title',
            slug='test-title',
            author=cls.user,
            content='Test content',
            status='published'
        )

    def test_homeless_list_view(self):
        response = self.client.get(reverse('homelessness_advice_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Title')
        self.assertTemplateUsed(response, 'homelessness_advice/homelessness_advice_list.html')

    def test_homeless_detail_view(self):
        response = self.client.get(reverse('homelessness_advice_detail', args=[self.homeless.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Title')
        self.assertTemplateUsed(response, 'homelessness_advice/homelessness_advice_detail.html')

    def test_homeless_detail_view_not_found(self):
        response = self.client.get(reverse('homelessness_advice_detail', args=['non-existent-slug']))
        self.assertEqual(response.status_code, 404)
