from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from testimonials.models import Testimonial

class TestimonialAdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser(username='admin', password='admin')
        cls.testimonial = Testimonial.objects.create(
            author=cls.user,
            body='Testimonial body'
        )

    def test_testimonial_admin_list_view(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin:testimonials_testimonial_changelist'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Testimonial body')

    def test_testimonial_admin_change_view(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin:testimonials_testimonial_change', args=[self.testimonial.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Testimonial body')
