from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15)



    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

    def __str__(self):
        return self.username