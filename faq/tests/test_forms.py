from django.test import TestCase
from faq.forms import CommentForm

class TestCommentForm(TestCase):

    def test_comment_form_valid_data(self):
        form = CommentForm(data={
            'body': 'This is a test comment'
        })

        self.assertTrue(form.is_valid())

    def test_comment_form_empty_data(self):
        form = CommentForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_comment_form_fields(self):
        form = CommentForm()
        self.assertEqual(list(form.fields), ['body'])
