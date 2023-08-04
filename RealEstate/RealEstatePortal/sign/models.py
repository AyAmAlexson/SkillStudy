from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from properties.models import CustomUser
from phonenumber_field.formfields import PhoneNumberField


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    phone_1 = PhoneNumberField(label="Phone #")

    class Meta:
        model = CustomUser
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "phone_1",
                  "password1",
                  "password2",)


from django.db import models

# Create your models here.
