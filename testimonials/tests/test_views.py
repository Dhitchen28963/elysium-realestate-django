from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from testimonials.models import Testimonial

class TestimonialViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user', password='password')
        cls.testimonial = Testimonial.objects.create(
            author=cls.user,
            body='Testimonial body'
        )

    def setUp(self):
        self.client.login(username='user', password='password')

    def test_testimonials_list_view(self):
        response = self.client.get(reverse('testimonials_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Testimonial body')

    def test_testimonials_detail_view(self):
        response = self.client.get(reverse('testimonials_detail', args=[self.testimonial.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Testimonial body')

    def test_add_testimonial_view(self):
        response = self.client.post(reverse('add_testimonial'), {
            'body': 'New testimonial body'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Testimonial.objects.count(), 2)

    def test_edit_testimonial_view(self):
        response = self.client.post(reverse('edit_testimonial', args=[self.testimonial.pk]), {
            'body': 'Updated testimonial body'
        })
        self.testimonial.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.testimonial.body, 'Updated testimonial body')

    def test_delete_testimonial_view(self):
        response = self.client.post(reverse('delete_testimonial', args=[self.testimonial.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Testimonial.objects.filter(pk=self.testimonial.pk).exists())
