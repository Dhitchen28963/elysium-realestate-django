from django.test import TestCase
from contact.forms import ContactForm

class ContactFormTest(TestCase):

    def test_valid_form(self):
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'message': 'Test Message'
        }
        form = ContactForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = ContactForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)
