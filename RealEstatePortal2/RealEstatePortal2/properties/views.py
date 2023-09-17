from datetime import datetime

from django.http import HttpResponse
from django.views import View

from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters import PropertyFilter, PropertyQuickFilter
from .forms import ResPropertyForm
from .models import ResProperties



class ResPropertiesList(LoginRequiredMixin, ListView):
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
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PropertyQuickFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_ordering(self):
        self.order = self.request.GET.get('order', 'asc')
        selected_ordering = self.request.GET.get('ordering', 'date_added')
        if self.order == "desc":
            selected_ordering = "-" + selected_ordering
        return selected_ordering

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
        context['current_order'] = self.get_ordering()
        context['order'] = self.order
        context['filterset'] = self.filterset

        return context


class ResPropertiesDetail(LoginRequiredMixin, DetailView):
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
        property_instance = self.object
        features = property_instance.prop_features.all()
        context['features'] = features
        return context

    def get_object(self, queryset=None):
        ref_oct = self.kwargs['ref_oct']
        ref = int(ref_oct, 8)  # Преобразование в десятичное число
        return get_object_or_404(ResProperties, ref=ref)

class ResPropertyCreateResidential(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = ResPropertyForm
    model = ResProperties
    template_name = 'resproperties_edit.html'
    permission_required = ('properties.add_resproperties',)

    def form_valid(self, form):
        resproperty = form.save(commit=False)
        resproperty.prop_division = "QL"
        return super().form_valid(form)


class ResPropertyCreateSales(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = ResPropertyForm
    model = ResProperties
    template_name = 'resproperties_edit.html'
    permission_required = ('properties.add_resproperties',)

    def form_valid(self, form):
        resproperty = form.save(commit=False)
        resproperty.prop_division = "ZH"
        return super().form_valid(form)


class ResPropertyCreateCommercial(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = ResPropertyForm
    model = ResProperties
    template_name = 'resproperties_edit.html'
    permission_required = ('properties.add_resproperties',)

    def form_valid(self, form):
        resproperty = form.save(commit=False)
        resproperty.prop_division = "QC"
        return super().form_valid(form)


class ResPropertyUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    form_class = ResPropertyForm
    model = ResProperties
    template_name = 'resproperties_edit.html'
    permission_required = ('properties.change_resproperties',)

    def get_object(self, queryset=None):
        ref_oct = self.kwargs['ref_oct']
        ref = int(ref_oct, 8)  # Преобразование в десятичное число
        return get_object_or_404(ResProperties, ref=ref)

class ResPropertyDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = ResProperties
    template_name = 'resproperties_delete.html'
    success_url = reverse_lazy('properties:properties_list')
    permission_required = ('properties.delete_resproperties',)

    def get_object(self, queryset=None):
        ref_oct = self.kwargs['ref_oct']
        ref = int(ref_oct, 8)  # Преобразование в десятичное число
        return get_object_or_404(ResProperties, ref=ref)

class ResPropertiesSearch(LoginRequiredMixin, ListView):
    model = ResProperties
    ordering = 'ref'
    template_name = 'resproperties_search.html'
    context_object_name = 'resproperties_search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PropertyFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_ordering(self):
        self.order = self.request.GET.get('order', 'asc')
        selected_ordering = self.request.GET.get('ordering', 'date_added')
        if self.order == "desc":
            selected_ordering = "-" + selected_ordering
        return selected_ordering

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['current_order'] = self.get_ordering()
        context['order'] = self.order
        context['filterset'] = self.filterset

        return context



