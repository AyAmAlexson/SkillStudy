
from RealEstatePortal2.settings import EMAIL_HOST_USER
from users.models import Subscriptions, CustomUser, CustomUser_Subscriptions
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models.signals import post_save

from .models import ResProperties

@receiver(post_save, sender = ResProperties)
def notify_subscribers_new_property(sender, instance, created, **kwargs):
    if created:

        try:
            subscriptions_list = Subscriptions.objects.filter(
                Q(sub_category=instance.prop_division) | Q(sub_category=""),
                Q(sub_area=instance.area) | Q(sub_area=""),
                Q(sub_max_price__gte=instance.price) | Q(sub_max_price__isnull=True),
                Q(sub_max_bedrooms__gte=instance.bedrooms) | Q(sub_max_bedrooms__isnull=True),
                sub_min_price__lte=instance.price,
                sub_min_bedrooms__lte=instance.bedrooms,
            )

            customusers_list = CustomUser.objects.filter(
                subscriptions__in=subscriptions_list
            )

            for customuser in customusers_list:
                html_content = render_to_string(
                    'emails/new_property_update.html',
                    {
                        'category': instance.prop_division,
                        'new_property': instance,
                        'customuser': customuser,
                    }
                )
                msg = EmailMultiAlternatives(
                    subject=f'QL Exiles: New Property Added - have a look!',
                    body='',
                    from_email=EMAIL_HOST_USER,
                    to=[f'{customuser.email}']
                )
                msg.attach_alternative(html_content, "text/html")  # добавляем html
                msg.send()  # отсылаем

        except ObjectDoesNotExist:
            print('Something went wrong, not sending')