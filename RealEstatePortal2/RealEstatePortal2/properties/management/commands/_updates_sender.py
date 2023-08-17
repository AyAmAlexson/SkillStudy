
from RealEstatePortal2.settings import EMAIL_HOST_USER
from users.models import Subscriptions, CustomUser, CustomUser_Subscriptions
from properties.models import ResProperties

from datetime import datetime, timedelta, timezone
import pytz

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


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