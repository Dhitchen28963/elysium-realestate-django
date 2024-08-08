from django.test import TestCase
from django.contrib.auth.models import User
from homelessness_advice.forms import HomelessForm
from homelessness_advice.models import Homeless

class HomelessFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user', password='password')

    def test_valid_form(self):
        form_data = {
            'title': 'Test Title',
            'slug': 'test-title',
            'author': self.user.id,
            'featured_image': 'sample-image.jpg',
            'content': 'Test content',
            'status': 'published',
            'excerpt': 'Test excerpt'
        }
        form = HomelessForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'title': '',
            'slug': '',
            'author': self.user.id,
            'featured_image': 'sample-image.jpg',
            'content': 'Test content',
            'status': 'published',
            'excerpt': 'Test excerpt'
        }
        form = HomelessForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('slug', form.errors)
