from datetime import date, time, timedelta
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from real_estate.models import Property, FavoriteProperty, ViewingSlot, ViewingAppointment

class PropertyViewTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass')
        self.client.login(username='testuser', password='testpass')
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
            agent=self.user
        )
        self.viewing_slot = ViewingSlot.objects.create(
            property=self.property,
            agent=self.user,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(11, 0),
            is_booked=False
        )

    def test_property_sale_view(self):
        response = self.client.get(reverse('property_sale'), {'search': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.property.title)
        self.assertIn(self.property, response.context['properties'])

    def test_property_detail_view(self):
        response = self.client.get(reverse('property_detail', args=[self.property.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.property.title)

    def test_request_custom_viewing(self):
        form_data = {
            'preferred_date': date.today().isoformat(),
            'preferred_time': time(10, 0).isoformat(),
            'name': 'Test User',
            'contact': '1234567890',
            'email': 'testuser@example.com',
            'message': 'I would like a viewing.'
        }
        response = self.client.post(
            reverse('request_custom_viewing', args=[self.property.id]),
            data=form_data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'ok'})
        self.assertEqual(ViewingAppointment.objects.count(), 1)

    def test_accept_appointment(self):
        appointment = ViewingAppointment.objects.create(
            user=self.user,
            property=self.property,
            name='Test User',
            email='testuser@example.com',
            preferred_date=date.today(),
            preferred_time=time(10, 0),
            viewing_decision='pending'
        )
        response = self.client.post(reverse('accept_appointment', args=[appointment.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ViewingAppointment.objects.get(id=appointment.id).viewing_decision, 'accepted')

    def test_add_to_favorites(self):
        response = self.client.post(reverse('add_to_favorites', args=[self.property.id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'ok'})
        self.assertTrue(FavoriteProperty.objects.filter(user=self.user, property=self.property).exists())

    def test_remove_from_favorites(self):
        FavoriteProperty.objects.create(user=self.user, property=self.property)
        response = self.client.post(reverse('remove_from_favorites', args=[self.property.id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'ok'})
        self.assertFalse(FavoriteProperty.objects.filter(user=self.user, property=self.property).exists())

    def test_view_favorites(self):
        FavoriteProperty.objects.create(user=self.user, property=self.property)
        response = self.client.get(reverse('view_favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.property.title)

    def test_account_settings_view(self):
        response = self.client.get(reverse('account_settings'))
        self.assertEqual(response.status_code, 200)

    def test_property_search(self):
        response = self.client.get(reverse('property_sale'), {'search': 'Test Location'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.property.title)

    def test_view_pending_viewings(self):
        ViewingAppointment.objects.create(
            user=self.user,
            property=self.property,
            name='Test User',
            email='testuser@example.com',
            preferred_date=date.today(),
            preferred_time=time(10, 0),
            viewing_decision='pending'
        )
        response = self.client.get(reverse('view_pending_viewings'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test User')

    def test_update_viewing(self):
        appointment = ViewingAppointment.objects.create(
            user=self.user,
            property=self.property,
            name='Test User',
            email='testuser@example.com',
            preferred_date=date.today(),
            preferred_time=time(10, 0),
            viewing_decision='pending'
        )
        response = self.client.post(reverse('update_viewing', args=[appointment.id]), {
            'preferred_date': (date.today() + timedelta(days=1)).isoformat(),
            'preferred_time': time(11, 0).isoformat(),
            'name': 'Test User',
            'contact': '1234567890',
            'email': 'testuser@example.com',
            'message': 'Updated message.'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ViewingAppointment.objects.get(id=appointment.id).preferred_date, date.today() + timedelta(days=1))

    def test_delete_viewing(self):
        appointment = ViewingAppointment.objects.create(
            user=self.user,
            property=self.property,
            name='Test User',
            email='testuser@example.com',
            preferred_date=date.today(),
            preferred_time=time(10, 0),
            viewing_decision='pending'
        )
        response = self.client.post(reverse('delete_viewing', args=[appointment.id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'ok'})
        self.assertFalse(ViewingAppointment.objects.filter(id=appointment.id).exists())
