from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone_1 = models.CharField(max_length=15)
    phone_2 = models.CharField(max_length=15, null=True)
    phone_3 = models.CharField(max_length=15, null=True)

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

    def __str__(self):
        return self.username
