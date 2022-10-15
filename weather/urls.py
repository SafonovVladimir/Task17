from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    # path('', get_user_subscriptions, name='home'),
    path('user/<slug:username>', get_user_subscriptions, name='user_subscriptions'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('check_username/', check_username, name='check_username'),
    path('validate_username/', validate_username, name='validate_username'),

    path('api/v1/subscriptions/', SubscriptionsAPIList.as_view()),
    path('api/v1/subscriptions/<int:pk>/', SubscriptionsAPIUpdate.as_view()),
    path('api/v1/subscriptionsdelete/<int:pk>/', SubscriptionsAPIDestroy.as_view()),

    path('api/v1/city/', CityAPIList.as_view()),
    path('api/v1/city/<int:pk>/', CityAPIUpdate.as_view()),
    path('api/v1/citydelete/<int:pk>/', CityAPIDestroy.as_view()),

    path('api/v1/forecast/', ForecastAPIList.as_view()),
    path('api/v1/forecast/<int:pk>/', ForecastAPIUpdate.as_view()),
    path('api/v1/forecastdelete/<int:pk>/', ForecastAPIDestroy.as_view()),

    path('add_subscription/', add_subscription, name='add_subscription'),
    path('view_city_forecast/', view_city_forecast, name='view_city_forecast'),
]
