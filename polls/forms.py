from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import SomeUser


class RegisterForm(UserCreationForm):
    img = forms.ImageField(required=False)

    class Meta:
        model = SomeUser
        fields = [
            'username',
            'img'
        ]
