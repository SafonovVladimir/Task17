from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_task():
    send_mail('Your city weather forecast!',
              'The weater in city ___ is ___!',
              'NOTIFICATION_EMAIL',
              ['vladimir_safonov@ukr.net'],
              fail_silently=False
              )
    return None
