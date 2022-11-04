from django.contrib import admin

from .models import *

admin.site.site_title = 'Manage Weather Reminder'
admin.site.site_header = 'Manage Weather Reminder'


class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'interval', 'created_at')
    list_display_links = ('id', 'user')
    search_fields = ('user',)
    save_on_top = True


class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'city_name')#, 'timezone', 'longitude', 'latitude')
    list_display_links = ('id', 'city_name')
    filter_horizontal = ['subscriptions']
    search_fields = ('city_name',)
    save_on_top = True


class ForecastAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'city', 'weather', 'temp', 'humidity', 'pressure', 'temp_min', 'temp_max', 'visibility', 'wind_speed',
    'clouds', 'sunrise', 'sunset')
    list_display_links = ('id', 'city')
    search_fields = ('city',)
    save_on_top = True


admin.site.register(Subscriptions, SubscriptionsAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Forecast, ForecastAdmin)
