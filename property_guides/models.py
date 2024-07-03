from django.db import models
from django.utils import timezone

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('Landlord', 'Landlord'),
        ('Renter', 'Renter'),
        ('Student', 'Student'),
        ('Neighbour Disputes', 'Neighbour Disputes'),
        ('Repairs', 'Repairs'),
        ('Fire Safety', 'Fire Safety'),
        ('Complaints', 'Complaints'),
        ('Eviction', 'Eviction'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    featured_image = models.ImageField(upload_to='images/', null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Landlord')

    def __str__(self):
        return self.title