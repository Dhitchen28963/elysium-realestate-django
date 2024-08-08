from django.test import TestCase, Client
from django.urls import reverse
from property_guides.models import Category, Post
from django.utils import timezone

class PropertyGuidesCategoryViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Test Category')

        Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is a test post for test category.',
            category=self.category,
            created_on=timezone.now(),
            updated_on=timezone.now(),
            featured_image='placeholder.jpg'
        )

    def test_property_guides_category_view(self):
        response = self.client.get(reverse('property_guides_category', kwargs={'category_name': 'Test Category'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
