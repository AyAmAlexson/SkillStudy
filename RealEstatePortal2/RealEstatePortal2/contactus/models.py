from django.db import models
from datetime import datetime


class PropertyEnquiry(models.Model):
    date_time = models.DateTimeField(
        auto_now_add=True
    )

    client_name = models.CharField(
        max_length=200
    )
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=15
    )
    property_ref = models.CharField(
        max_length=7,
        null=True
    )
    comment = models.TextField()

    def __str__(self):
        return f'{self.client_name} at {self.date_time}'
