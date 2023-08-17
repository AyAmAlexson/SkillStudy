
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from phonenumber_field.formfields import PhoneNumberField



class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user

class AccountDetailsForm(forms.ModelForm):

    user_name = forms.CharField(max_length=50)
    user_fname = forms.CharField(max_length=50)
    user_lname = forms.CharField(max_length=50)
    user_email  = forms.EmailField()
    user_phone1 = PhoneNumberField()
    user_phone2 = PhoneNumberField()
    user_phone3 = PhoneNumberField()
    user_password = forms.CharField(max_length=32,widget=forms.PasswordInput)



    class Meta:
        model = CustomUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_1',
            'phone_2',
            'phone_3',
            'password',
        ]

