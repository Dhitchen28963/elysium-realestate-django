from django.test import TestCase
from testimonials.forms import TestimonialForm

class TestimonialFormTests(TestCase):
    def test_valid_form(self):
        form_data = {
            'body': 'This is a valid testimonial body.'
        }
        form = TestimonialForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'body': ''
        }
        form = TestimonialForm(data=form_data)
        self.assertFalse(form.is_valid())
