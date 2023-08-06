from django_filters import FilterSet,DateFromToRangeFilter
from django.forms import DateInput
import django_filters
from .models import ResProperties
from django import forms
from .misc import PROP_DIVISION_CHOICES, LOCATION_CHOICES



# Создаем свой набор фильтров для модели ResProperties.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PropertyFilter(FilterSet):
    ref = django_filters.NumberFilter(lookup_expr='icontains', label='REF #',widget=forms.NumberInput(attrs={'class':'form-control'}))
    location = django_filters.ChoiceFilter(
        field_name='location',
        choices=LOCATION_CHOICES,
        label="Location",
        empty_label="All Locations",
        widget=forms.widgets.Select(attrs={'class':'form-control'})
    )
    _price_min = django_filters.NumberFilter(field_name='_price',label='Price MIN:', lookup_expr='gt',widget=forms.NumberInput(attrs={'class':'form-control'}))
    _price_max = django_filters.NumberFilter(field_name='_price',label='Price MAX:', lookup_expr='lt',widget=forms.NumberInput(attrs={'class':'form-control'}))
    prop_division = django_filters.ChoiceFilter(choices=PROP_DIVISION_CHOICES, label="Division:",empty_label="All Divisions", widget=forms.Select(attrs={'class':'form-control'}))
    date_added = django_filters.DateFilter(lookup_expr='gt', label="Added after date:", widget=DateInput(
        attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd','class':'form-control'}))

    class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
        model = ResProperties
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
        fields = ['prop_division','ref','_price_min','_price_max','location','date_added']



class PropertyQuickFilter(FilterSet):
    prop_division = django_filters.ChoiceFilter(choices=PROP_DIVISION_CHOICES, label="Division:",
                                                empty_label="All Divisions",
                                                widget=forms.Select())
    class Meta:

        model = ResProperties
        fields = {
            'prop_division':[],
            'ref': ['icontains'],
        }

