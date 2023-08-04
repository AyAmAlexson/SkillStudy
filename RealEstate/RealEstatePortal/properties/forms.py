from django import forms
from .models import ResProperties, Features, Agents
from django.core.exceptions import ValidationError
from .misc import LOCATION_CHOICES

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class ResPropertyForm(forms.ModelForm):
    ref = forms.NumberInput(attrs={'class': 'form-control'})
    _price = forms.FloatField(min_value=0.0, label="Price")
    location = forms.ChoiceField(choices=LOCATION_CHOICES)
    prop_features = forms.ModelMultipleChoiceField(
        label="Features",
        widget=forms.CheckboxSelectMultiple,
        queryset=Features.objects.all()
    )

    class Meta:
        model = ResProperties
        fields = [
            'ref',
            'prop_type',
            'location',
            'address',
            '_price',
            'status',
            'bedrooms',
            'bathrooms',
            'prop_features',
            'prop_description',
            'owner',
            'added_by'
        ]


    def clean(self):
        cleaned_data = super().clean()
        ref = cleaned_data.get("ref")
        _price = cleaned_data.get("_price")

        if ref is not None and (int(ref) < 200 or int(ref)>200000):
            raise ValidationError({
                "ref": "Invalid ref number"
            })
        return cleaned_data





