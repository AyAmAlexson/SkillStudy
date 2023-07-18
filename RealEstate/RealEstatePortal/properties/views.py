from django.views.generic import ListView, DetailView
from .models import ResProperties,Features,PropertiesFeatures
from django.shortcuts import render
from datetime import datetime
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

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = None
        return context


class ResPropertiesDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = ResProperties
    # Используем другой шаблон — product.html
    template_name = 'resproperty.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'resproperty'
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = None
        return context

