import datetime
import json
import urllib.request

from celery import shared_task
from django.core.mail import send_mail

from Task17.settings import API_KEY
from weather.models import City, Forecast


@shared_task
def send_email(interval):
    cities = City.objects.all()
    for city in cities:
        for sub in city.subscriptions.all():
            if sub.interval == interval:
                source = urllib.request.urlopen(
                    f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric').read()
                list_of_data = json.loads(source)
                weather = str(list_of_data['weather'][0]['main'])
                country_code = str(list_of_data['sys']['country'])
                longitude = str(list_of_data['coord']['lon'])
                latidude = str(list_of_data['coord']['lat'])
                timezone = str(list_of_data['timezone'] // 3600)
                temperature = str(list_of_data['main']['temp'])
                temp_min = str(list_of_data['main']['temp_min'])
                temp_max = str(list_of_data['main']['temp_max'])
                pressure = str(list_of_data['main']['pressure'])
                humidity = str(list_of_data['main']['humidity'])
                feels_like = str(list_of_data['main']['feels_like'])
                visibility = str(list_of_data['visibility'])
                wind_speed = str(list_of_data['wind']['speed'])
                clouds = str(list_of_data['clouds']['all'])
                sunrise = datetime.datetime.fromtimestamp(list_of_data['sys']['sunrise']).strftime('%H:%M:%S')
                sunset = datetime.datetime.fromtimestamp(list_of_data['sys']['sunset']).strftime('%H:%M:%S')

                context = f"Thanks to our service, you get a weather forecast in the city {city} once every {interval} hours." \
                          f"<h3>country_code: {country_code}</h3>" \
                          f"<p>timezone: {timezone}</p>" \
                          f"<p>longitude: {longitude}, latidude: {latidude}</p>" \
                          f"<br>" \
                          f"<p>weather: {weather}</p>" \
                          f"<p>temperature: {temperature + 'C'}, temperature min: {temp_min + 'C'}, temperature max: {temp_max + 'C'}</p>" \
                          f"<p>feels_like: {feels_like}</p>" \
                          f"<br>" \
                          f"<p>pressure: {pressure}, humidity: {humidity}, visibility: {visibility}</p>" \
                          f"<p>wind speed: {wind_speed}, clouds: {clouds}</p>" \
                          f"<p>sunrise: {sunrise}, sunset: {sunset}</p>"
                f, created = Forecast.objects.get_or_create(
                    city=city,
                    weather=weather,
                    temp=temperature,
                    humidity=humidity,
                    pressure=pressure,
                    temp_min=temp_min,
                    temp_max=temp_max,
                    visibility=visibility,
                    wind_speed=wind_speed,
                    clouds=clouds,
                    sunrise=sunrise,
                    sunset=sunset,
                )
                send_mail(f'Forecast in {city}!',
                          f'The weather in {city}:',
                          'Weather Reminder Service',
                          [sub.user.email],
                          html_message=context,
                          fail_silently=False
                          )
