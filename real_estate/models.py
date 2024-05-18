from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Property(models.Model):
    PROPERTY_TYPES = [
        ('flat', 'Flat'),
        ('house', 'House'),
        ('boat', 'Boat'),
        ('land', 'Land'),
        ('other', 'Other'),
    ]

    FURNISHED_TYPES = [
        ('furnished', 'Furnished'),
        ('unfurnished', 'Unfurnished'),
        ('part_furnished', 'Part Furnished'),
    ]

    TRANSACTION_TYPES = [
        ('rent', 'Rent'),
        ('buy', 'Buy'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    furnished_type = models.CharField(max_length=20, choices=FURNISHED_TYPES)
    location = models.CharField(max_length=255)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    garden = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    pets_allowed = models.BooleanField(default=False)
    property_image = models.ImageField(upload_to='property_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def price_display(self):
        if self.transaction_type == 'rent':
            return f"{self.price} PCM"
        return f"{self.price}"