from django.contrib.auth.models import User
from django import forms
from .models import Route

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
    #DateTimeInput - текст бокс с форматированием
    #https://docs.djangoproject.com/en/1.10/ref/forms/widgets/
    time = forms.DateTimeField(widget=forms.DateTimeInput(format='%H:%M %d-%m-%Y'))

    class Meta:
        model = Route
        fields = ['load_title', 'load_weight', 'time']