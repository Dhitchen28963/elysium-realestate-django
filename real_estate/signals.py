from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Property, Profile
from django.contrib.auth.models import User


"""
Signal receiver that creates a Profile instance for a new User upon creation.
"""


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


"""
Signal receiver saves the Profile associated with a User whenever its saved.
"""


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
