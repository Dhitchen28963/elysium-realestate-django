from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from property_guides.models import Post, Category
from django.utils import timezone

class PostListViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Landlord')
        Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is a test post.',
            category=self.category,
            created_on=timezone.now(),
            updated_on=timezone.now(),
            featured_image='placeholder.jpg'
        )

    def test_post_list_view(self):
        response = self.client.get(reverse('property_guides_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')


class PostDetailViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Test Category')
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is a test post.',
            category=self.category,
            created_on=timezone.now(),
            updated_on=timezone.now(),
            featured_image='placeholder.jpg'
        )

    def test_post_detail_view(self):
        response = self.client.get(reverse('property_guides_detail', args=[self.post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')


class PropertyGuidesCategoryViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.category_repairs = Category.objects.create(name='Repairs')
        self.category_fire_safety = Category.objects.create(name='Fire Safety')
        self.category_complaints = Category.objects.create(name='Complaints')
        self.category_eviction = Category.objects.create(name='Eviction')

        Post.objects.create(
            title='Test Post Repairs',
            slug='test-post-repairs',
            content='This is a test post for repairs.',
            category=self.category_repairs,
            created_on=timezone.now(),
            updated_on=timezone.now(),
            featured_image='placeholder.jpg'
        )

        Post.objects.create(
            title='Test Post Fire Safety',
            slug='test-post-fire-safety',
            content='This is a test post for fire safety.',
            category=self.category_fire_safety,
            created_on=timezone.now(),
            updated_on=timezone.now(),
            featured_image='placeholder.jpg'
        )

        Post.objects.create(
            title='Test Post Complaints',
            slug='test-post-complaints',
            content='This is a test post for complaints.',
            category=self.category_complaints,
            created_on=timezone.now(),
            updated_on=timezone.now(),
            featured_image='placeholder.jpg'
        )

        Post.objects.create(
            title='Test Post Eviction',
            slug='test-post-eviction',
            content='This is a test post for eviction.',
            category=self.category_eviction,
            created_on=timezone.now(),
            updated_on=timezone.now(),
            featured_image='placeholder.jpg'
        )

    def test_property_guides_category_view_repairs(self):
        response = self.client.get(reverse('repairs'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post Repairs')

    def test_property_guides_category_view_fire_safety(self):
        response = self.client.get(reverse('fire_safety'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post Fire Safety')

    def test_property_guides_category_view_complaints(self):
        response = self.client.get(reverse('complaints'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post Complaints')

    def test_property_guides_category_view_eviction(self):
        response = self.client.get(reverse('eviction'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post Eviction')
