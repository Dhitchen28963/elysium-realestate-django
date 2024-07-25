from django.test import TestCase
from django.contrib.auth.models import User
from property_guides.models import Post, Category, PropertyImage


class CategoryModelTest(TestCase):

    def test_create_category(self):
        category = Category.objects.create(name='Test Category')
        self.assertEqual(category.name, 'Test Category')
        self.assertEqual(str(category), 'Test Category')


class PostModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Test Category')

    def test_create_post(self):
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is a test post.',
            category=self.category
        )
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.slug, 'test-post')
        self.assertEqual(post.category.name, 'Test Category')
        self.assertEqual(str(post), 'Test Post')


class PropertyImageModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is a test post.',
            category=self.category
        )

    def test_create_property_image(self):
        property_image = PropertyImage.objects.create(
            post=self.post,
            image='test_image.jpg'
        )
        self.assertEqual(property_image.post.title, 'Test Post')
        self.assertEqual(property_image.image, 'test_image.jpg')
        self.assertEqual(str(property_image), 'Image for Test Post')
