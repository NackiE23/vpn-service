from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.text import slugify

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="user/avatar/%Y/%m", blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. "
                                         "Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    description = models.TextField(max_length=550, blank=True, null=True)


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


class Statistics(models.Model):
    site = models.OneToOneField(Site, on_delete=models.CASCADE)
    page_transitions = models.IntegerField(default=0)
    data_sent = models.DecimalField(default=0, decimal_places=3, max_digits=12)
    data_downloaded = models.DecimalField(default=0, decimal_places=3, max_digits=12)
