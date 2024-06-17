
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
from .models import Property, SavedSearch, PropertyAlert, Profile
from django.contrib.auth.models import User

@receiver(post_save, sender=Property)
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

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()