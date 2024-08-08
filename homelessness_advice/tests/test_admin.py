from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from homelessness_advice.models import Homeless, HomelessImage

class HomelessAdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser(username='admin', password='admin')
        cls.homeless = Homeless.objects.create(
            title='Test Homeless',
            slug='test-homeless',
            author=cls.user,
            content='Test content',
            status='published'
        )
        cls.homeless_image = HomelessImage.objects.create(
            homeless=cls.homeless,
            image='sample-image.jpg'
        )

    def test_homeless_admin_change_view(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin:homelessness_advice_homeless_change', args=[self.homeless.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Homeless')

    def test_homeless_admin_list_view(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin:homelessness_advice_homeless_changelist'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Homeless')

    def test_homeless_image_inline(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('admin:homelessness_advice_homeless_change', args=[self.homeless.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'sample-image.jpg')
