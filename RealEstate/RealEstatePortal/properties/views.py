from django.views.generic import ListView, DetailView
from .models import ResProperties
from django.shortcuts import render

# Create your views here.
class ResPropertiesList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = ResProperties
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'date_added'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'resproperties.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'resproperties'

class ResPropertiesDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = ResProperties
    # Используем другой шаблон — product.html
    template_name = 'resproperty.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'resproperty'