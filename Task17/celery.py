import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Task17.settings')

app = Celery('Task17')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    # 'every-10-minutes': {
    #     'task': 'weather.tasks.send_email',
    #     "schedule": crontab(minute="*/10"),
    # },
    'every-1-hour': {
        'task': 'weather.tasks.send_email',
        "schedule": crontab(minute="*/1"),
        'args': ('1H',)
    },
    # 'every-3-hours': {
    #     'task': 'weather.tasks.send_email',
    #     "schedule": crontab(hour="*/3"),
    # },
    # 'every-6-hours': {
    #     'task': 'weather.tasks.send_email',
    #     "schedule": crontab(hour="*/6"),
    # },
    # 'every-12-hours': {
    #     'task': 'weather.tasks.send_email',
    #     "schedule": crontab(hour="*/12"),
    # },
    # 'every-24-hours': {
    #     'task': 'weather.tasks.send_email',
    #     "schedule": crontab(hour="*/24"),
    # },
}

app.autodiscover_tasks()
