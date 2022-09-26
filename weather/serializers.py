from rest_framework import serializers

from .models import Subscriptions, City, Forecast


class SubscriptionsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Subscriptions
        fields = ('__all__')


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('__all__')


class ForecastSerializer(serializers.ModelSerializer):

    class Meta:
        model = Forecast
        fields = ('__all__')