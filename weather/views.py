import json
import urllib.request

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from Task17.settings import API_KEY
from .forms import UserLoginForm, UserRegisterForm, AddSubscriptionForm, AddCityForm
from .models import City, Subscriptions, Forecast
from .permissions import IsAdminOrReadOnly
from .serializers import SubscriptionsSerializer, CitySerializer, ForecastSerializer


def index(request):
    if request.user.is_authenticated:
        return redirect('user_subscriptions', request.user.username)
    else:
        return redirect('login')


def add_interval(request):
    user = request.user
    if request.method == 'POST':
        subscribe = AddSubscriptionForm(request.POST)
        context = {
            'subscribe': subscribe,
        }
        if subscribe.is_valid():
            instance = subscribe.save(commit=False)
            instance.user = user
            instance.save()
            return redirect('add_subscription')
        else:
            messages.error(request, 'Error')
    else:
        subscribe = AddSubscriptionForm()
        context = {
            'subscribe': subscribe,
        }
    return render(request, "weather/add_interval.html", context=context)


def add_subscription(request):
    user = request.user
    user_id = User.objects.get(username=user.username).id
    if request.method == 'POST':
        intervals = AddSubscriptionForm(request.POST)
        city = AddCityForm(request.POST)
        context = {
            'city': city,
            'intervals': intervals,
        }
        if city.is_valid():
            instance_interval = intervals.save(commit=False)
            instance_interval.user = user
            instance_interval.save()
            # intervals.save()
            instance_city = city.save(commit=False)
            instance_city.save()
            instance_city.subscriptions.add(instance_interval)
            # instance_interval.save()
            return redirect('user_subscriptions', user)
        else:
            messages.error(request, 'Error')
    else:
        city = AddCityForm()
        intervals = AddSubscriptionForm()
        context = {
            'city': city,
            'intervals': intervals,
        }
    return render(request, "weather/add_subscription.html", context=context)


def view_city_forecast(request):
    if request.method == 'POST':
        city = request.POST['city']
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
    else:
        context = {
        }
    return render(request, "weather/view_forecast.html", context=context)


def get_user_subscriptions(request, username):
    user_id = User.objects.get(username=username).id
    subscriptions = Subscriptions.objects.filter(user=user_id).order_by('created_at')
    # intervals = Subscriptions.INTERVAL_CHOICES

    context = {
        "subscriptions": subscriptions,
        # "intervals": intervals,
    }
    return render(request, "weather/index.html", context=context)

def delete_subscription(request, id):
    city = get_object_or_404(City, pk=id)
    if request.method == 'POST':         # If method is POST,
        city.delete()
        return redirect('home')             # Finally, redirect to the index page.

    return render(request, 'weather/index.html', {'city': city})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('user_subscriptions', user)
            # return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'weather/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        context = {
            'form': form,
        }
        if form.is_valid():
            user = form.save()
            # Profile.objects.create(user=form.instance)
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Error')
    else:
        form = UserRegisterForm()
        context = {
            'form': form,
        }
    return render(request, 'weather/register.html', context=context)


def validate_username(request):
    """Check available name"""
    username = request.GET.get('username', None)
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(response)


def check_username(request):
    """Check username"""
    username = request.GET.get('username', None)
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(response)


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


class SubscriptionsView(CreateView):
    model = Subscriptions
