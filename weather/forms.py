from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Subscriptions, City


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='User name', widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={"class": "form-control"}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label='Confirm password',
                                widget=forms.PasswordInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class AddSubscriptionForm(forms.ModelForm):

    class Meta:
        model = Subscriptions
        fields = ['interval']

class AddCityForm(forms.ModelForm):

    class Meta:
        model = City
        fields = ['city_name', 'subscriptions']

        # city_name = forms.CharField()
        # subscriptions = forms.ModelMultipleChoiceField(
        #     queryset=Subscriptions.objects.all(),
        #     widget=forms.CheckboxSelectMultiple
        # )



