import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RealEstatePortal2.settings')

app = Celery('RealEstatePortal2')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'sending_new_prop_summary_every_monday_8am': {
        'task': 'properties.tasks.send_weekly_property_updates',
        'schedule': crontab(hour=6, minute=00, day_of_week='Monday'),
        #'args': (),
    },
}

app.autodiscover_tasks()