from django.test import TestCase
from django.contrib.auth.models import User
from testimonials.models import Testimonial

class TestimonialModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user', password='password')
        cls.testimonial = Testimonial.objects.create(
            author=cls.user,
            body='Testimonial body'
        )

    def test_testimonial_str_method(self):
        self.assertEqual(str(self.testimonial), f'Testimonial by {self.user.username}')

    def test_testimonial_creation(self):
        self.assertEqual(self.testimonial.body, 'Testimonial body')
        self.assertEqual(self.testimonial.author.username, 'user')
