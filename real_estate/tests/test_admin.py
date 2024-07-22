from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.admin.sites import site
from django.urls import reverse
from real_estate.models import (
    Property, PropertyImage, ViewingSlot, FavoriteProperty, ViewingAppointment
)
from real_estate.admin import PropertyAdmin, ViewingSlotAdmin, FavoritePropertyAdmin, ViewingAppointmentAdmin
from datetime import date, time

class AdminSiteTests(TestCase):

    def setUp(self):
        # Create a superuser
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
        # Create related objects
        self.property = Property.objects.create(
            title='Test Property',
            description='A test property',
            property_type='detached-houses',
            price=100000.00,
            furnished_type='unfurnished',
            location='Test Location',
            transaction_type='sale',
            bedrooms=3,
            bathrooms=2,
            garden=True,
            parking=True,
            pets_allowed=True,
            energy_efficiency_rating='A',
            availability_status='available',
            publication_status='published',
            agent=self.superuser
        )
        self.property_image = PropertyImage.objects.create(
            property=self.property,
            image='test_image.jpg'
        )
        self.viewing_slot = ViewingSlot.objects.create(
            agent=self.superuser,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(11, 0),
            is_booked=False
        )
        self.favorite_property = FavoriteProperty.objects.create(
            user=self.superuser,
            property=self.property
        )
        self.viewing_appointment = ViewingAppointment.objects.create(
            user=self.superuser,
            property=self.property,
            name='John Doe',
            email='johndoe@example.com',
            preferred_date=date.today(),
            preferred_time=time(9, 0),
            viewing_decision='pending'
        )

    def test_property_admin_list_display(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('admin:real_estate_property_changelist'))
        self.assertContains(response, 'Test Property')
        self.assertContains(response, 'Test Location')
        self.assertContains(response, '£100,000.00')  # Expecting the formatted price with currency

    def test_viewing_slot_admin_display(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('admin:real_estate_viewingslot_changelist'))
        self.assertContains(response, self.viewing_slot.start_time)
        self.assertContains(response, self.viewing_slot.end_time)
        self.assertContains(response, self.viewing_slot.agent.username)

    def test_favorite_property_admin_display(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('admin:real_estate_favoriteproperty_changelist'))
        self.assertContains(response, self.favorite_property.user.username)
        self.assertContains(response, self.favorite_property.property.title)

    def test_viewing_appointment_admin_display(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('admin:real_estate_viewingappointment_changelist'))
        self.assertContains(response, self.viewing_appointment.user.username)
        self.assertContains(response, self.viewing_appointment.property.title)
        self.assertContains(response, self.viewing_appointment.name)

    def test_viewing_appointment_actions(self):
        self.client.login(username='admin', password='adminpassword')
        # Test marking as attended
        response = self.client.post(
            reverse('admin:real_estate_viewingappointment_changelist'),
            {'action': 'mark_as_attended', '_selected_action': [self.viewing_appointment.id]}
        )
        self.viewing_appointment.refresh_from_db()
        self.assertTrue(self.viewing_appointment.attended)

        # Test marking as not attended
        self.viewing_appointment.attended = True
        self.viewing_appointment.save()
        response = self.client.post(
            reverse('admin:real_estate_viewingappointment_changelist'),
            {'action': 'mark_as_not_attended', '_selected_action': [self.viewing_appointment.id]}
        )
        self.viewing_appointment.refresh_from_db()
        self.assertFalse(self.viewing_appointment.attended)

        # Test accepting viewing
        self.viewing_appointment.viewing_decision = 'pending'
        self.viewing_appointment.save()
        response = self.client.post(
            reverse('admin:real_estate_viewingappointment_changelist'),
            {'action': 'accept_viewing', '_selected_action': [self.viewing_appointment.id]}
        )
        self.viewing_appointment.refresh_from_db()
        self.assertEqual(self.viewing_appointment.viewing_decision, 'accepted')

        # Test rejecting viewing
        self.viewing_appointment.viewing_decision = 'pending'
        self.viewing_appointment.save()
        response = self.client.post(
            reverse('admin:real_estate_viewingappointment_changelist'),
            {'action': 'reject_viewing', '_selected_action': [self.viewing_appointment.id]}
        )
        self.viewing_appointment.refresh_from_db()
        self.assertEqual(self.viewing_appointment.viewing_decision, 'rejected')
