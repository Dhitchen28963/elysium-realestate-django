from datetime import date, time
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from django_summernote.fields import SummernoteTextField
from .utils import clean_html_content
from django.db.models.signals import post_save
from django.dispatch import receiver


# Choices for the furnished status of a property
FURNISHED_TYPES = [
    ('furnished', 'Furnished'),
    ('unfurnished', 'Unfurnished'),
    ('part_furnished', 'Part Furnished'),
]


"""
Model representing a Property.
Includes fields for title, slug, description, type, price, location,
and other property-specific attributes.
"""


class Property(models.Model):
    TYPE_CHOICES = [
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
        ('student', 'Student Accommodation'),
        ('land', 'Land'),
    ]

    PROPERTY_TYPE_CHOICES = [
        ('detached-houses', 'Detached houses'),
        ('semi-detached-houses', 'Semi-detached houses'),
        ('terraced-houses', 'Terraced houses'),
        ('mobile-park-homes', 'Mobile / Park homes'),
        ('boats', 'Boats'),
        ('flats-apartments', 'Flats / Apartments'),
        ('bungalows', 'Bungalows'),
        ('land', 'Land'),
        ('commercial-property', 'Commercial Property'),
        ('hmo', 'HMO\'s'),
    ]

    TRANSACTION_TYPES = [
        ('rent', 'Rent'),
        ('sale', 'Sale'),
        ('student', 'Student Accommodation'),
        ('land', 'Land'),
    ]

    PUBLICATION_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    AVAILABILITY_STATUS_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = SummernoteTextField()
    property_type = models.CharField(
        max_length=20, choices=PROPERTY_TYPE_CHOICES
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    furnished_type = models.CharField(max_length=20, choices=FURNISHED_TYPES)
    location = models.CharField(max_length=100)
    transaction_type = models.CharField(
        max_length=8, choices=TRANSACTION_TYPES
    )
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    garden = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    pets_allowed = models.BooleanField(default=False)
    floor_plan = models.ImageField(
        upload_to='floor_plans/', blank=True, null=True
    )
    energy_efficiency_rating = models.CharField(
        max_length=10, blank=True, null=True
    )
    availability_status = models.CharField(
        max_length=15, choices=AVAILABILITY_STATUS_CHOICES, default='available'
    )
    publication_status = models.CharField(
        max_length=10, choices=PUBLICATION_STATUS_CHOICES, default='draft'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    agent = models.ForeignKey(
        User, on_delete=models.CASCADE, default=1, related_name='properties'
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Property, self).save(*args, **kwargs)

    @property
    def price_display(self):
        formatted_price = f"£{self.price:,.2f}"
        if self.transaction_type == 'rent':
            return f"{formatted_price} PCM"
        return formatted_price


"""
Model representing images associated with a property.
Uses Cloudinary to store images.
"""


class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property, related_name='property_images', on_delete=models.CASCADE
    )
    image = CloudinaryField('image')

    def __str__(self):
        return f"{self.property.title} Image"


"""
Model representing a user's favorite property.
Each user can mark properties as their favorite.
"""


class FavoriteProperty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')

    def __str__(self):
        return f"{self.user.username} - {self.property.title}"


"""
Model representing a viewing slot for a property.
Agents can set available slots for potential viewers.
"""


class ViewingSlot(models.Model):
    property = models.ForeignKey(
        Property, related_name='viewing_slots', on_delete=models.CASCADE,
        null=True
    )
    agent = models.ForeignKey(
        User, related_name='agent_slots', on_delete=models.CASCADE, default=1
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        property_title = (
            self.property.title if self.property else "No Property"
        )
        return (
            f"{property_title} on {self.date} from "
            f"{self.start_time} to {self.end_time}"
        )


"""
Model representing a viewing appointment.
Stores the details of appointments scheduled for property viewings.
"""


class ViewingAppointment(models.Model):
    VIEWING_DECISION_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.ForeignKey(
        ViewingSlot, on_delete=models.SET_NULL, null=True, blank=True
    )
    name = models.CharField(max_length=255, default='Anonymous')
    contact = models.CharField(max_length=255, default='Unknown')
    email = models.EmailField(default='example@example.com')
    message = models.TextField(default='No message')
    preferred_date = models.DateField(default=date.today)
    preferred_time = models.TimeField(default=time(9, 0))
    is_scheduled = models.BooleanField(default=False)
    attended = models.BooleanField(default=False)
    viewing_decision = models.CharField(
        max_length=10, choices=VIEWING_DECISION_CHOICES, default='pending'
    )
    created_on = models.DateTimeField(auto_now_add=True)
    agent_name = models.CharField(max_length=255, blank=True, null=True)
    agent_contact = models.CharField(max_length=255, blank=True, null=True)
    agent_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return (
            f"Viewing Appointment for {self.property.title} "
            f"by {self.name}"
        )


"""
Model representing a user's profile.
Stores additional user information such as name, email, address, and telephone.
"""


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255)
    telephone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username


# Signal receiver to handle updates on ViewingAppointment
@receiver(post_save, sender=ViewingAppointment)
def update_profile_on_viewing_decision(sender, instance, **kwargs):
    if kwargs.get('update_fields') and \
            'viewing_decision' in kwargs.get('update_fields'):
        if instance.viewing_decision == 'accepted':
            print(
                f"Appointment for {instance.property.title} "
                f"has been accepted."
            )
        elif instance.viewing_decision == 'rejected':
            # Handle rejected appointments
            print(
                f"Appointment for {instance.property.title} "
                f"has been rejected."
            )
