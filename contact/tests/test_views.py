from django.test import TestCase, Client
from django.urls import reverse
from contact.models import ContactMessage

class ContactMessageViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_contact_message_view_get(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')

    def test_contact_message_view_post(self):
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'message': 'Test Message'
        }
        response = self.client.post(reverse('contact'), data)
        self.assertEqual(response.status_code, 200)  # JSON response
        self.assertTrue(ContactMessage.objects.filter(email='john@example.com').exists())
        self.assertEqual(response.json(), {'success': True})

    def test_contact_message_view_post_invalid(self):
        data = {
            'name': '',
            'email': '',
            'message': ''
        }
        response = self.client.post(reverse('contact'), data)
        self.assertEqual(response.status_code, 200)  # JSON response
        self.assertEqual(response.json()['success'], False)
        self.assertIn('name', response.json()['errors'])
        self.assertIn('email', response.json()['errors'])
        self.assertIn('message', response.json()['errors'])
