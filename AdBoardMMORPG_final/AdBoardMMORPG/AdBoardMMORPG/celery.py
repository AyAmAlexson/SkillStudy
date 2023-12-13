import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AdBoardMMORPG.settings')

app = Celery('AdBoardMMORPG')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'sending_news_prop_summary_every_monday_11am': {
        'task': 'Ads.tasks.send_weekly_news',
        'schedule': crontab(hour=11, minute=00, day_of_week='Monday'),
        #'args': (),
    },
}

app.autodiscover_tasks()