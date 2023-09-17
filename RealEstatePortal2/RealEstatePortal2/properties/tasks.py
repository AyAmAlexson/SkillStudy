from celery import shared_task
from .models import ResProperties
from datetime import datetime, timedelta, timezone
import pytz
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from RealEstatePortal2.settings import EMAIL_HOST_USER
from users.models import Subscriptions, CustomUser, CustomUser_Subscriptions





def send_property_updates_mails():
    print("Here i send update emails")


@shared_task
def send_weekly_property_updates():
    tz = pytz.timezone("Europe/Malta")
    current_datetime = datetime.now(tz)
    subs = Subscriptions.objects.all()
    try:
        for sub in subs:
            props = ResProperties.objects.filter(
                _price__gte=sub.sub_min_price,
                bedrooms__gte=sub.sub_min_bedrooms,
                date_added__gte=current_datetime - timedelta(weeks=1)
            )
            if sub.sub_category:
                props = props.filter(prop_division = sub.sub_category)
            if sub.sub_max_price:
                props = props.filter(prop_price__lte=sub.sub_max_price)
            if sub.sub_max_bedrooms:
                props = props.filter(bedrooms__lte=sub.sub_max_bedrooms)
            if sub.sub_area:
                props = props.filter(area=sub.sub_area)

            customusers_list = CustomUser.objects.filter(
                subscriptions__in=[sub]
            )

            for customuser in customusers_list:
                html_content = render_to_string(
                    'emails/weekly_property_update.html',
                    {
                        'property_list': props,
                        'customuser': customuser,
                        'sub': sub,
                    }
                )
                msg = EmailMultiAlternatives(
                    subject=f'QL Exiles: Your weekly property updates',
                    body='',
                    from_email=EMAIL_HOST_USER,
                    to=[f'{customuser.email}']
                )
                msg.attach_alternative(html_content, "text/html")  # добавляем html
                msg.send()  # отсылаем

    except ObjectDoesNotExist:
        print('Something went wrong, not sending')

@shared_task
def notify_subscribers_new_property(pid, created, **kwargs):
    if created:
        try:
            instance = ResProperties.objects.get(id=pid)
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