from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

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
