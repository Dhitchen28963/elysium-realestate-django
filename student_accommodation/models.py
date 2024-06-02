from datetime import date, time
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

FURNISHED_TYPES = [
    ('furnished', 'Furnished'),
    ('unfurnished', 'Unfurnished'),
    ('part_furnished', 'Part Furnished'),
]

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

class StudentProperty(models.Model):
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
    agent = models.ForeignKey(User, related_name='student_properties', on_delete=models.CASCADE, default=1)
    availability_status = models.CharField(max_length=15, choices=[('available', 'Available'), ('unavailable', 'Unavailable')], default='available')
    publication_status = models.CharField(max_length=10, choices=[('draft', 'Draft'), ('published', 'Published')], default='draft')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class StudentPropertyImage(models.Model):
    property = models.ForeignKey(StudentProperty, related_name='property_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='student_property_images/')

    def __str__(self):
        return f"{self.property.title} Image"

class FavoriteProperty(models.Model):
    user = models.ForeignKey(User, related_name='student_favorite_properties', on_delete=models.CASCADE)
    property = models.ForeignKey(StudentProperty, related_name='favorites', on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')

    def __str__(self):
        return f"{self.user.username} - {self.property.title}"

class StudentPropertyMessage(models.Model):
    property = models.ForeignKey(StudentProperty, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='student_property_messages', on_delete=models.CASCADE)
    agent = models.ForeignKey(User, related_name='student_agent_messages', on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} about {self.property.title}"

class ViewingSlot(models.Model):
    property = models.ForeignKey(StudentProperty, related_name='viewing_slots', on_delete=models.CASCADE)
    agent = models.ForeignKey(User, related_name='student_agent_slots', on_delete=models.CASCADE)
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

    property = models.ForeignKey(StudentProperty, related_name='appointments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='student_viewing_appointments', on_delete=models.CASCADE)
    slot = models.ForeignKey(ViewingSlot, related_name='appointments', on_delete=models.SET_NULL, null=True, blank=True)
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
    agent_name = models.CharField(max_length=255, blank=True, null=True)
    agent_contact = models.CharField(max_length=255, blank=True, null=True)
    agent_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"Viewing Appointment for {self.property.title} by {self.name}"

class SavedSearch(models.Model):
    user = models.ForeignKey(User, related_name='student_saved_searches', on_delete=models.CASCADE)
    search_name = models.CharField(max_length=255)
    location = models.CharField(max_length=100, blank=True, null=True)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, blank=True, null=True)
    bedrooms_min = models.PositiveIntegerField(blank=True, null=True)
    bedrooms_max = models.PositiveIntegerField(blank=True, null=True)
    bathrooms_min = models.PositiveIntegerField(blank=True, null=True)
    bathrooms_max = models.PositiveIntegerField(blank=True, null=True)
    price_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    garden = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    pets_allowed = models.BooleanField(default=False)
    furnished_type = models.CharField(max_length=20, choices=FURNISHED_TYPES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.search_name}"

class PropertyAlert(models.Model):
    user = models.ForeignKey(User, related_name='student_property_alerts', on_delete=models.CASCADE)
    property = models.ForeignKey(StudentProperty, related_name='alerts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f"Alert for {self.user.username} - {self.property.title}"

@receiver(post_save, sender=StudentProperty)
def create_property_alert(sender, instance, created, **kwargs):
    if created:
        saved_searches = SavedSearch.objects.filter(
            Q(location__icontains=instance.location) | Q(location=''),
            Q(property_type=instance.property_type) | Q(property_type=''),
            Q(bedrooms_min__lte=instance.bedrooms) | Q(bedrooms_min__isnull=True),
            Q(bedrooms_max__gte=instance.bedrooms) | Q(bedrooms_max__isnull=True),
            Q(bathrooms_min__lte=instance.bathrooms) | Q(bathrooms_min__isnull=True),
            Q(bathrooms_max__gte=instance.bathrooms) | Q(bathrooms_max__isnull=True),
            Q(price_min__lte=instance.price) | Q(price_min__isnull=True),
            Q(price_max__gte=instance.price) | Q(price_max__isnull=True),
            garden=instance.garden,
            parking=instance.parking,
            pets_allowed=instance.pets_allowed,
            furnished_type=instance.furnished_type
        )
        for search in saved_searches:
            PropertyAlert.objects.create(user=search.user, property=instance)
