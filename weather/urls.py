from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('api/v1/subscriptions/', SubscriptionsAPIList.as_view()),
    path('api/v1/subscriptions/<int:pk>/', SubscriptionsAPIUpdate.as_view()),
    path('api/v1/subscriptionsdelete/<int:pk>/', SubscriptionsAPIDestroy.as_view()),

    path('api/v1/city/', CityAPIList.as_view()),
    path('api/v1/city/<int:pk>/', CityAPIUpdate.as_view()),
    path('api/v1/citydelete/<int:pk>/', CityAPIDestroy.as_view()),

    path('api/v1/forecast/', ForecastAPIList.as_view()),
    path('api/v1/forecast/<int:pk>/', ForecastAPIUpdate.as_view()),
    path('api/v1/forecastdelete/<int:pk>/', ForecastAPIDestroy.as_view()),
]
