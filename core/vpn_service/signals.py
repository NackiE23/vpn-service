from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Statistics

User = get_user_model()


@receiver(post_save, sender=User)
def create_statistics(sender, instance, created, **kwargs):
    if created:
        Statistics.objects.create(user=instance)
