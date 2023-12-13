from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import mail_managers
from .models import Ad, Response, Category
from users.models import Subscription

from .tasks import notify_subscribers_new_ad, notify_ad_author_new_response, notify_response_author_result


@receiver(post_save, sender = Ad)
def send_notification_new_ad(sender, instance, created, **kwargs):
    notify_subscribers_new_ad.delay(instance.id, created)

@receiver(post_save, sender = Category)
def add_new_subscription(sender, instance, created, **kwargs):
    if created:
        try:
            Subscription.objects.create(sub_category=instance.id)
        except:
            print('Something Went Wrong on Adding New Sub')

@receiver(post_save, sender = Response)
def send_notification_on_response(sender, instance, created, **kwargs):
    notify_ad_author_new_response.delay(instance.id, created)

@receiver(pre_save, sender=Response)
def send_notification_on_response_result(sender, instance, **kwargs):
    # Проверяем, изменилось ли поле status
    if instance.pk:
        old_instance = Response.objects.get(pk=instance.pk)
        if old_instance.status != instance.status:
            # Поле изменилось, выполняем необходимые действия
            notify_response_author_result.delay(instance.id, instance.status)






