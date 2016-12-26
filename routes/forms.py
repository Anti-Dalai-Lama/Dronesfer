from django.contrib.auth.models import User
from django import forms
from .models import Route
from datetime import datetime, timedelta

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

class CreateRouteForm(forms.ModelForm):
    time = forms.DateTimeField(widget=forms.DateTimeInput(format='%H:%M %d.%m.%Y'), initial=datetime.now() + timedelta(hours=1), input_formats=['%H:%M %d.%m.%Y'])
    load_title = forms.CharField(initial='Your load')
    load_weight = forms.DecimalField(initial=0, decimal_places=3, max_digits=6, max_value=10)

    class Meta:
        model = Route
        fields = ['load_title', 'load_weight', 'time']


class UpdateRouteForm(forms.ModelForm):
    time = forms.DateTimeField(widget=forms.DateTimeInput(format='%H:%M %d.%m.%Y'), input_formats=['%H:%M %d.%m.%Y'])
    load_title = forms.CharField()
    load_weight = forms.DecimalField(decimal_places=3, max_digits=6, max_value=10)

    class Meta:
        model = Route
        fields = ['load_title', 'load_weight', 'time']