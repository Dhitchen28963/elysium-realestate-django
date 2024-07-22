from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
from real_estate.forms import (
    PropertySearchForm,
    ViewingAppointmentForm,
    ProfileUpdateForm,
    ChangePasswordForm,
    DeleteAccountForm
)
from real_estate.models import Property, ViewingAppointment, Profile

class PropertySearchFormTest(TestCase):
    def test_form_validity(self):
        form_data = {
            'search': 'Test Location',
            'location': 'Test Location',
            'property_type': 'any',
            'bedrooms_min': 1,
            'bedrooms_max': 3,
            'price_min': 100000,
            'price_max': 500000,
            'garden': True,
            'parking': False,
            'pets_allowed': True
        }
        form = PropertySearchForm(data=form_data)
        self.assertTrue(form.is_valid())

class ViewingAppointmentFormTest(TestCase):
    def test_form_validity(self):
        form_data = {
            'name': 'John Doe',
            'contact': '1234567890',
            'email': 'john@example.com',
            'preferred_date': date.today() + timedelta(days=1),
            'preferred_time': '10:00',
            'message': 'Looking forward to the viewing.'
        }
        form = ViewingAppointmentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_preferred_date(self):
        form_data = {
            'name': 'John Doe',
            'contact': '1234567890',
            'email': 'john@example.com',
            'preferred_date': date.today() - timedelta(days=1),
            'preferred_time': '10:00',
            'message': 'Looking forward to the viewing.'
        }
        form = ViewingAppointmentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('preferred_date', form.errors)

    def test_form_past_date(self):
        form_data = {
            'name': 'John Doe',
            'contact': '1234567890',
            'email': 'john.doe@example.com',
            'preferred_date': date.today() - timedelta(days=1),  # a past date
            'preferred_time': '10:00',
            'message': 'I would like to view the property.'
        }
        form = ViewingAppointmentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('preferred_date', form.errors)

class ProfileUpdateFormTest(TestCase):
    def test_form_validity(self):
        # Create a user and associate a profile with it
        user = User.objects.create_user(username='testuser', password='password')
        # Ensures the creation of one profile per user
        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults={
                'name': 'John Doe',
                'email': 'john@example.com',
                'address': '123 Street',
                'telephone': '1234567890'
            }
        )
        form_data = {
            'name': 'John Doe Updated',
            'email': 'john_updated@example.com',
            'address': '456 Avenue',
            'telephone': '0987654321'
        }
        form = ProfileUpdateForm(instance=profile, data=form_data)
        self.assertTrue(form.is_valid())

class ChangePasswordFormTest(TestCase):
    def test_form_validity(self):
        # Create a user
        user = User.objects.create_user(username='testuser', password='old_password')
        
        form_data = {
            'old_password': 'old_password',
            'new_password1': 'new_password',
            'new_password2': 'new_password'
        }
        form = ChangePasswordForm(user=user, data=form_data)
        self.assertTrue(form.is_valid())

class DeleteAccountFormTest(TestCase):
    def test_form_validity(self):
        form_data = {
            'confirm_delete': True
        }
        form = DeleteAccountForm(data=form_data)
        self.assertTrue(form.is_valid())
