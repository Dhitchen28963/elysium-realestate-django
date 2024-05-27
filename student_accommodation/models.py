from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class StudentProperty(models.Model):
    PROPERTY_TYPES = [
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

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    furnished_type = models.CharField(max_length=20, choices=FURNISHED_TYPES)
    location = models.CharField(max_length=255)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    garden = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    pets_allowed = models.BooleanField(default=False)
    property_image = models.ImageField(upload_to='student_accommodation_images/', default='default.jpg')
    floor_plan = models.ImageField(upload_to='floor_plans/', blank=True, null=True)
    energy_efficiency_rating = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=15, choices=[('available', 'Available'), ('unavailable', 'Unavailable')], default='available')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title