from django.contrib.auth import get_user_model
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.text import slugify

User = get_user_model()


class Statistics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    page_transitions = models.IntegerField(default=0)
    data_sent = models.IntegerField(default=0)
    data_downloaded = models.IntegerField(default=0)


class Site(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    url = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        unique_slug = self.slug or slugify(self.name)
        while self.__class__.objects.filter(slug=unique_slug).exists():
            unique_slug += get_random_string(length=4)
        self.slug = unique_slug
        super().save(*args, **kwargs)
