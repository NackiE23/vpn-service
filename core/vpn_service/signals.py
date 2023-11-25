from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, UserProfile, Site, Statistics


@receiver(post_save, sender=User)
def create_userprofile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=Site)
def create_statistics(sender, instance, created, **kwargs):
    if created:
        Statistics.objects.create(site=instance)
