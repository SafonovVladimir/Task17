import urllib.request
from django.shortcuts import render
import json

from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from weather.models import City, Subscriptions, Forecast
from weather.permissions import IsAdminOrReadOnly
from weather.serializers import SubscriptionsSerializer, CitySerializer, ForecastSerializer

API_KEY = '601e4e6a7e92e77aa8f999a053b5510f'


def index(request):
    if request.method == 'POST':
        city = request.POST['city']

        source = urllib.request.urlopen(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric').read()

        list_of_data = json.loads(source)

        # data for variable list_of_data
        context = {
            "country_code": str(list_of_data['sys']['country']),
            "longitude": str(list_of_data['coord']['lon']),
            "latidude": str(list_of_data['coord']['lat']),
            "timezone": str(list_of_data['timezone'] // 3600),
            "temp": str(list_of_data['main']['temp']) + 'C',
            "pressure": str(list_of_data['main']['pressure']),
            "humidity": str(list_of_data['main']['humidity']),
            "code": str(list_of_data['cod']),
            "list_of_data": list_of_data,
        }
        # print(context)
    else:
        context = {}

    return render(request, "weather/index.html", context=context)


class SubscriptionsAPIListPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10000


class CityAPIListPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10000


class ForecastAPIListPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10000


class SubscriptionsAPIList(generics.ListCreateAPIView):
    queryset = Subscriptions.objects.all()
    serializer_class = SubscriptionsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = SubscriptionsAPIListPagination


class SubscriptionsAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Subscriptions.objects.all()
    serializer_class = SubscriptionsSerializer
    permission_classes = (IsAuthenticated,)
    # permission_classes = (IsOwnerOrReadOnly,)


class SubscriptionsAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Subscriptions.objects.all()
    serializer_class = SubscriptionsSerializer
    permission_classes = (IsAdminOrReadOnly,)


class CityAPIList(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = CityAPIListPagination


class CityAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (IsAuthenticated,)


class CityAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (IsAdminOrReadOnly,)


class ForecastAPIList(generics.ListCreateAPIView):
    queryset = Forecast.objects.all()
    serializer_class = ForecastSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = ForecastAPIListPagination


class ForecastAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Forecast.objects.all()
    serializer_class = ForecastSerializer
    permission_classes = (IsAuthenticated,)


class ForecastAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Forecast.objects.all()
    serializer_class = ForecastSerializer
    permission_classes = (IsAdminOrReadOnly,)
