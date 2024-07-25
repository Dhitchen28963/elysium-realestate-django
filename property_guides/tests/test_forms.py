from django.test import TestCase
from property_guides.forms import PostForm


class TestPostForm(TestCase):

    def test_post_form_valid_data(self):
        form = PostForm(data={
            'title': 'Test Post',
            'slug': 'test-post',
            'content': 'This is a test post.',
        })

        self.assertTrue(form.is_valid())

    def test_post_form_empty_data(self):
        form = PostForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)  # Assuming title, slug, and content are required

    def test_post_form_fields(self):
        form = PostForm()
        self.assertEqual(list(form.fields), ['title', 'slug', 'featured_image', 'content'])
