from django.dispatch import receiver
from django.db.models.signals import post_save
from .tasks import notify_subscribers_new_property

from .models import ResProperties

@receiver(post_save, sender = ResProperties)
def send_notification_on_creation(sender, instance, created, **kwargs):
    notify_subscribers_new_property.delay(instance.id, created)
