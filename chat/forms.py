from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Room


class RegisterForm(UserCreationForm):
    """Simple registration form using Django's built-in UserCreationForm"""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class RoomForm(forms.ModelForm):
    """Form to create a new chat room"""
    class Meta:
        model = Room
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g. General, Tech Talk, Random'})
        }
