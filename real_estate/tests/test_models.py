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

class ProfileModelTests(TestCase):

    def setUp(self):
        # Clean up existing profiles and users to avoid conflicts
        Profile.objects.all().delete()
        User.objects.all().delete()

        # Create a new user and profile
        self.user = User.objects.create_user(
            username='johndoe',
            email='johndoe@example.com',
            password='password'
        )
        self.profile, created = Profile.objects.get_or_create(
            user=self.user,
            defaults={
                'name': 'John Doe',
                'address': '123 Main Street',
                'telephone': '1234567890'
            }
        )

    def test_string_representation(self):
        self.assertEqual(str(self.profile), 'johndoe')

    def tearDown(self):
        # Clean up after each test
        Profile.objects.all().delete()
        User.objects.all().delete()
