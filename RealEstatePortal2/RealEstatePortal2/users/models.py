from django.contrib.auth.models import AbstractUser
from django.db import models
from properties.misc import AREAS_CHOICES, PROP_DIVISION, PROP_DIVISION_REFERENCE, PROP_STATUSES, PROP_DIVISION_CHOICES, rented, residential, commercial, sales, soon, available, to_call



class CustomUser(AbstractUser):
    phone_1 = models.CharField(max_length=15)
    phone_2 = models.CharField(max_length=15, null=True)
    phone_3 = models.CharField(max_length=15, null=True)
    subscriptions = models.ManyToManyField('Subscriptions', through='CustomUser_Subscriptions')


    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

    def __str__(self):
        return self.username


class Subscriptions(models.Model):
    sub_category = models.CharField(max_length=2, choices=PROP_DIVISION_CHOICES, default="QL", null=True)
    sub_area = models.CharField(max_length=15, choices=AREAS_CHOICES, null=True)
    sub_min_price = models.IntegerField(default=0)
    sub_max_price = models.IntegerField(null=True)
    sub_min_bedrooms = models.IntegerField(default=0)
    sub_max_bedrooms = models.IntegerField(null=True)

    def __str__(self):
        return f'Subscription {self.id}: Category - {PROP_DIVISION_REFERENCE[self.sub_category or "All"]}, Area - {self.sub_area or "All"}, ' \
               f'Price range - {self.sub_min_price}-{self.sub_max_price or "Max"}, ' \
               f'Bedrooms - {self.sub_min_bedrooms}-{self.sub_max_bedrooms or "Max"}'

class CustomUser_Subscriptions(models.Model):
    sub_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sub_subscription = models.ForeignKey(Subscriptions, on_delete=models.CASCADE)