from celery import shared_task
from .models import Ad, Response
from datetime import datetime, timedelta, timezone
import pytz
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from AdBoardMMORPG.settings import EMAIL_HOST_USER
from users.models import Subscription, CustomUser, CustomUser_Subscription


def send_ad_and_response_updates_mails():
    print("Here i send update emails")

@shared_task
def notify_subscribers_new_ad(pid, created, **kwargs):
    if created:
        try:
            instance = Ad.objects.get(id=pid)
            subscriptions_list = Subscription.objects.filter(sub_category=instance.category)

            customusers_list = CustomUser.objects.filter(subscriptions__in=subscriptions_list)
            for customuser in customusers_list:
                html_content = render_to_string(
                    'emails/new_property_update.html',
                    {
                        'category': instance.category,
                        'ad': instance,
                        'customuser': customuser,
                    }
                )
                msg = EmailMultiAlternatives(
                    subject=f'AdBoard MMORPG: New Ad Added - have a look!',
                    body='',
                    from_email=EMAIL_HOST_USER,
                    to=[f'{customuser.email}']
                )
                msg.attach_alternative(html_content, "text/html")  # добавляем html
                msg.send()  # отсылаем

        except ObjectDoesNotExist:
            print('Something went wrong, not sending')


@shared_task
def notify_ad_author_new_response(pid, created, **kwargs):
    if created:
        try:
            instance = Response.objects.get(id=pid)
            ad_author = CustomUser.objects.get(id=instance.ad.author.id)
            html_content = render_to_string(
                'emails/new_response_update.html',
                {
                    'ad_author': ad_author,
                    'response': instance,
                    'ad': instance.ad,
                }
            )
            msg = EmailMultiAlternatives(
                subject=f'AdBoard MMORPG: New Response Added - have a look!',
                body='',
                from_email=EMAIL_HOST_USER,
                to=[f'{ad_author.email}']
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html
            msg.send()  # отсылаем


        except ObjectDoesNotExist:
            print('Something went wrong, not sending')


@shared_task
def notify_response_author_result(pid, **kwargs):
    is_withdrawn = False
    is_accepted = False
    try:
        instance = Response.objects.get(id=pid)
        ad_author = CustomUser.objects.get(id=instance.ad.author.id)
        response_author = CustomUser.objects.get(id=instance.author.id)
        if instance.status == 'WD':
            is_withdrawn = True
            is_accepted = False
        elif instance.status == 'RJ':
            is_withdrawn = False
            is_accepted = False
        elif instance.status == 'ED':
            is_withdrawn = False
            is_accepted = True

        html_content = render_to_string(
            'emails/response_result.html',
            {
                'ad_author': ad_author,
                'response': instance,
                'ad': instance.ad,
                'accepted': is_accepted,
                'withdrawn': is_withdrawn,
            }
        )
        msg = EmailMultiAlternatives(
            subject=f'AdBoard MMORPG: New Response Added - have a look!',
            body='',
            from_email=EMAIL_HOST_USER,
            to=[f'{response_author.email}']
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()  # отсылаем


    except ObjectDoesNotExist:
        print('Something went wrong, not sending')

@shared_task
def send_weekly_news():
    tz = pytz.timezone("Europe/Malta")
    current_datetime = datetime.now(tz)
    news_sub = Subscription.objects.get(sub_category=5) #Подписка на новости
    try:
        customusers_list = CustomUser.objects.filter(subscriptions=news_sub)

        for customuser in customusers_list:
            html_content = render_to_string(
                'emails/weekly_news_update.html',
                {
                    'customuser': customuser,
                    'sub': news_sub,
                }
            )
            msg = EmailMultiAlternatives(
                subject=f'QL Exiles: Your weekly news update',
                body='',
                from_email=EMAIL_HOST_USER,
                to=[f'{customuser.email}']
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html
            msg.send()  # отсылаем

    except ObjectDoesNotExist:
        print('Something went wrong, not sending')