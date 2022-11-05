import json
import urllib.request

from celery import shared_task
from django.core.mail import send_mail

from Task17.settings import API_KEY
from weather.models import City


@shared_task
def send_email(interval):
    cities = City.objects.all()
    for city in cities:
        for sub in city.subscriptions.all():
            if sub.interval == interval:
                source = urllib.request.urlopen(
                    f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric').read()
                list_of_data = json.loads(source)
                context = f"<h3>country_code: {str(list_of_data['sys']['country'])}</h3>" \
                          f"<p>longitude: {str(list_of_data['coord']['lon'])}</p>" \
                          f"<p>latidude: {str(list_of_data['coord']['lat'])}</p>" \
                          f"<p>timezone: {str(list_of_data['timezone'] // 3600)}</p>" \
                          f"<p>temperature: {str(list_of_data['main']['temp']) + 'C'}</p>" \
                          f"<p>pressure: {str(list_of_data['main']['pressure'])}</p>" \
                          f"<p>humidity: {str(list_of_data['main']['humidity'])}</p>"
                send_mail(f'Forecast in {city}!',
                          f'The weather in {city}:',
                          'Weather Reminder Service',
                          [sub.user.email],
                          html_message=context,
                          fail_silently=False
                          )
