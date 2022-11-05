import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Task17.settings')

app = Celery('Task17')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'every-1-hour': {
        'task': 'weather.tasks.send_email',
        "schedule": crontab(minute="*/2"),
        'args': ('1H',)
    },
    'every-3-hours': {
        'task': 'weather.tasks.send_email',
        "schedule": crontab(hour="*/3"),
        'args': ('3H',)
    },
    'every-6-hours': {
        'task': 'weather.tasks.send_email',
        "schedule": crontab(hour="*/6"),
        'args': ('6H',)
    },
    'every-12-hours': {
        'task': 'weather.tasks.send_email',
        "schedule": crontab(hour="*/12"),
        'args': ('12H',)
    },
    'every-24-hours': {
        'task': 'weather.tasks.send_email',
        "schedule": crontab(hour="*/24"),
        'args': ('24H',)
    },
}

app.autodiscover_tasks()
