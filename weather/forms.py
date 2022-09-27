from django import forms
from .models import Subscriptions, City, Forecast
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


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

