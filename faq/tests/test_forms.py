from django.test import TestCase
from faq.forms import CommentForm

class CommentFormTest(TestCase):

    def test_valid_form(self):
        data = {
            'body': 'This is a test comment.'
        }
        form = CommentForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
