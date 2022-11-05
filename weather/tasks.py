import json
import urllib.request

from celery import shared_task
from django.core.mail import send_mail

from Task17.settings import API_KEY
from weather.models import City


@shared_task
def send_email():
    cities = City.objects.all()
    for city in cities:
        source = urllib.request.urlopen(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric').read()
        list_of_data = json.loads(source)
        context = {
            "country_code": str(list_of_data['sys']['country']),
            "longitude": str(list_of_data['coord']['lon']),
            "latidude": str(list_of_data['coord']['lat']),
            "timezone": str(list_of_data['timezone'] // 3600),
            "temp": str(list_of_data['main']['temp']) + 'C',
            "pressure": str(list_of_data['main']['pressure']),
            "humidity": str(list_of_data['main']['humidity']),
            "code": str(list_of_data['cod']),
        }
        send_mail(f'Forecast in {city}!',
                  f'The weather in {city}: \n{context}',
                  'Weather Reminder Service',
                  ['vladimir_safonov@ukr.net'],
                  fail_silently=False
                  )

# @shared_task
# def send_email(email):
#     send_mail('Forecast in city!',
#               'The weater in city ___ is ___!',
#               'NOTIFICATION_EMAIL',
#               [email],
#               fail_silently=False
#               )
