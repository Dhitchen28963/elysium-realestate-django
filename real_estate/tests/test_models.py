from django.test import TestCase
from django.contrib.auth.models import User
from real_estate.models import (
    Property, PropertyImage, FavoriteProperty, ViewingSlot, ViewingAppointment, Profile
)
from datetime import date, time

class PropertyModelTests(TestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
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

    def test_string_representation(self):
        self.assertEqual(str(self.property), 'Test Property')

    def test_price_display(self):
        self.assertEqual(self.property.price_display, '£100,000.00')
        
        self.property.transaction_type = 'rent'
        self.property.save()
        self.assertEqual(self.property.price_display, '£100,000.00 PCM')

    def test_slug_creation(self):
        self.assertEqual(self.property.slug, 'test-property')

    def test_auto_slug_creation_on_save(self):
        self.property.slug = ''
        self.property.save()
        self.assertEqual(self.property.slug, 'test-property')

class PropertyImageModelTests(TestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
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
            image='test_image.jpg'  # Ensure you have a valid image path or mock this field
        )

    def test_string_representation(self):
        self.assertEqual(str(self.property_image), 'Test Property Image')

class FavoritePropertyModelTests(TestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
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
        self.favorite_property = FavoriteProperty.objects.create(
            user=self.superuser,
            property=self.property
        )

    def test_string_representation(self):
        self.assertEqual(str(self.favorite_property), 'admin - Test Property')

    def test_unique_together(self):
        # Ensure the unique constraint is working by trying to create a duplicate
        with self.assertRaises(Exception):
            FavoriteProperty.objects.create(
                user=self.superuser,
                property=self.property
            )

class ViewingSlotModelTests(TestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
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
        self.viewing_slot = ViewingSlot.objects.create(
            property=self.property,
            agent=self.superuser,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(11, 0),
            is_booked=False
        )

    def test_string_representation(self):
        expected_str = f"Test Property on {self.viewing_slot.date} from {self.viewing_slot.start_time} to {self.viewing_slot.end_time}"
        self.assertEqual(str(self.viewing_slot), expected_str)

    def test_booking_status(self):
        self.assertFalse(self.viewing_slot.is_booked)
        self.viewing_slot.is_booked = True
        self.viewing_slot.save()
        self.assertTrue(ViewingSlot.objects.get(id=self.viewing_slot.id).is_booked)

class ViewingAppointmentModelTests(TestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
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
        self.viewing_appointment = ViewingAppointment.objects.create(
            user=self.superuser,
            property=self.property,
            name='John Doe',
            email='johndoe@example.com',
            preferred_date=date.today(),
            preferred_time=time(9, 0),
            viewing_decision='pending'
        )

    def test_string_representation(self):
        expected_str = f"Viewing Appointment for Test Property by John Doe"
        self.assertEqual(str(self.viewing_appointment), expected_str)

    def test_viewing_decision(self):
        self.assertEqual(self.viewing_appointment.viewing_decision, 'pending')
        self.viewing_appointment.viewing_decision = 'accepted'
        self.viewing_appointment.save()
        self.assertEqual(ViewingAppointment.objects.get(id=self.viewing_appointment.id).viewing_decision, 'accepted')

class ProfileModelTests(TestCase):

    def setUp(self):
        Profile.objects.all().delete()
        User.objects.all().delete()

        self.user = User.objects.create_user(
            username='johndoe',
            email='johndoe@example.com',
            password='password'
        )
        # Ensure no previous profile exists for the user
        Profile.objects.filter(user=self.user).delete()
        
        # Create a profile for the user
        self.profile = Profile.objects.create(
            user=self.user,
            name='John Doe',
            address='123 Main Street',
            telephone='1234567890'
        )

    def test_string_representation(self):
        self.assertEqual(str(self.profile), 'johndoe')

    def test_profile_creation(self):
        self.assertTrue(self.profile)
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.name, 'John Doe')
        self.assertEqual(self.profile.address, '123 Main Street')
        self.assertEqual(self.profile.telephone, '1234567890')

    def test_profile_update(self):
        self.profile.name = 'Jane Doe'
        self.profile.save()
        self.assertEqual(Profile.objects.get(id=self.profile.id).name, 'Jane Doe')

    def tearDown(self):
        Profile.objects.all().delete()
        User.objects.all().delete()
