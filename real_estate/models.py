from datetime import date, time
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone

class Property(models.Model):
    TYPE_CHOICES = [
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
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

    FURNISHED_TYPES = [
        ('furnished', 'Furnished'),
        ('unfurnished', 'Unfurnished'),
        ('part_furnished', 'Part Furnished'),
    ]

    TRANSACTION_TYPES = [
        ('rent', 'Rent'),
        ('sale', 'Sale'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    furnished_type = models.CharField(max_length=20, choices=FURNISHED_TYPES)
    location = models.CharField(max_length=100)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    garden = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    pets_allowed = models.BooleanField(default=False)
    property_image = models.ImageField(upload_to='properties/')
    floor_plan = models.ImageField(upload_to='floor_plans/', blank=True, null=True)
    energy_efficiency_rating = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Property, self).save(*args, **kwargs)

    @property
    def price_display(self):
        if self.transaction_type == 'rent':
            return f"{self.price} PCM"
        return f"{self.price}"


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='property_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')

    def __str__(self):
        return f"{self.property.title} Image"


class FavoriteProperty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')

    def __str__(self):
        return f"{self.user.username} - {self.property.title}"


class PropertyMessage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} about {self.property.title}"


class ViewingSlot(models.Model):
    property = models.ForeignKey(Property, related_name='viewing_slots', on_delete=models.CASCADE)
    agent = models.ForeignKey(User, related_name='agent_slots', on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.property.title} on {self.date} from {self.start_time} to {self.end_time}"


class ViewingAppointment(models.Model):
    VIEWING_DECISION_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]


    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.ForeignKey(ViewingSlot, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255, default='Anonymous')
    contact = models.CharField(max_length=255, default='Unknown')
    email = models.EmailField(default='example@example.com')
    message = models.TextField(default='No message')
    preferred_date = models.DateField(default=date.today)
    preferred_time = models.TimeField(default=time(9, 0))
    is_scheduled = models.BooleanField(default=False)
    attended = models.BooleanField(default=False)
    viewing_decision = models.CharField(max_length=10, choices=VIEWING_DECISION_CHOICES, default='pending')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Viewing Appointment for {self.property.title} by {self.name}"

