from django.contrib.auth.models import User
from django.db import models


class Subscriptions(models.Model):
    INTERVAL_CHOICES = (
        ('1H', '1H'),
        ('3H', '3H'),
        ('6H', '6H'),
        ('12H', '12H'),
        ('24H', '24H'),
    )
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    interval = models.CharField("Interval", choices=INTERVAL_CHOICES, max_length=3, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Create')

    def __str__(self):
        # return str(self.pk)
        return self.user.get_username() + '_' + self.interval


    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        ordering = ['-created_at']


class City(models.Model):
    subscriptions = models.ManyToManyField(Subscriptions, blank=True, related_name='subscriptions')
    city_name = models.CharField("City name", blank=True, max_length=150)
    # timezone = models.CharField("Timezone", blank=False, max_length=10)
    # longitude = models.CharField("Longitude", blank=False, max_length=12)
    # latitude = models.CharField("Latitude", blank=False, max_length=12)

    def __str__(self):
        return self.city_name

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"


class Forecast(models.Model):
    city = models.ForeignKey(City, verbose_name="City", on_delete=models.CASCADE)
    weather = models.CharField("Weather", blank=True, max_length=150)
    temp = models.CharField("Temperature", blank=True, max_length=5)
    humidity = models.CharField("Humidity", blank=True, max_length=5)
    pressure = models.CharField("Pressure", blank=True, max_length=5)
    temp_min = models.CharField("Min temperature", blank=True, max_length=5)
    temp_max = models.CharField("Max temperature", blank=True, max_length=5)
    visibility = models.CharField("Visibility", blank=True, max_length=20)
    wind_speed = models.CharField("Wind speed", blank=True, max_length=10)
    clouds = models.CharField("Clouds", blank=True, max_length=35)
    sunrise = models.TimeField("Sunrise", blank=True, max_length=35)
    sunset = models.TimeField("Sunset", blank=True, max_length=35)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = "Forecast"
        verbose_name_plural = "Forecasts"
