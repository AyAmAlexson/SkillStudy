from django.contrib.auth.models import AbstractUser

from django.db import models


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15)
    subscriptions = models.ManyToManyField('Subscription', through='CustomUser_Subscription')


    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

    def __str__(self):
        return self.username

class Subscription(models.Model):
    sub_category = models.ForeignKey('Ads.Category', on_delete=models.CASCADE)


class CustomUser_Subscription(models.Model):
    sub_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sub_subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)