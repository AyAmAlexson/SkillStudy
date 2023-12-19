from django_filters import FilterSet,DateFromToRangeFilter
from django.forms import DateInput
import django_filters
from .models import Ad, Response, Category
from django import forms
from django.db.models import Q



class AdsFilter(FilterSet):


    category = django_filters.ModelChoiceFilter(
        field_name='category',
        label='Category',
        queryset=Category.objects.all(),
        empty_label='Все Категории',
        widget=forms.widgets.Select(attrs={'class': 'form-control'})
    )

    search_contents = django_filters.CharFilter(
        lookup_expr='icontains',
        method='filter_search_contents',
        label='Search Contents',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


    date_created = django_filters.DateFilter(
        lookup_expr='gt',
        label="Added after date:",
        widget=DateInput(
        attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd','class':'form-control'}))

    class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
        model = Ad
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
        fields = [
            'category',
            'search_contents',
            'date_created',
        ]

    def filter_search_contents(self, queryset, name, value):
        return queryset.filter(Q(body__icontains=value) | Q(title__icontains=value))

