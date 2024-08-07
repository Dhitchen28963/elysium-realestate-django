from django.test import TestCase
from contact.models import ContactMessage

class ContactMessageModelTest(TestCase):

    def test_string_representation(self):
        message = ContactMessage(name='John Doe', email='john@example.com', message='Test Message')
        self.assertEqual(str(message), 'Message from John Doe (john@example.com)')

    def test_create_contact_message(self):
        message = ContactMessage.objects.create(name='John Doe', email='john@example.com', message='Test Message')
        self.assertEqual(message.name, 'John Doe')
        self.assertEqual(message.email, 'john@example.com')
        self.assertEqual(message.message, 'Test Message')
