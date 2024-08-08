from django.test import TestCase
from django.contrib.auth.models import User
from homelessness_advice.models import Homeless, HomelessImage

class HomelessModelTests(TestCase):
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

    def test_homeless_str_method(self):
        self.assertEqual(str(self.homeless), 'Test Title')

    def test_homeless_image_str_method(self):
        homeless_image = HomelessImage.objects.create(
            homeless=self.homeless,
            image='sample-image.jpg'
        )
        self.assertEqual(str(homeless_image), 'Image for Test Title')

    def test_homeless_default_status(self):
        homeless = Homeless.objects.create(
            title='Another Test Title',
            slug='another-test-title',
            author=self.user,
            content='Another test content'
        )
        self.assertEqual(homeless.status, 'draft')
