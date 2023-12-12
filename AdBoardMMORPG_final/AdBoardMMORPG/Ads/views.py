from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from .forms import AdCreationForm
from .models import Ad, Image, Video

from Ads.models import Ad, Image, Video

from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from .custommixins import UserIsOwnerMixin





class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdCreationForm
    template_name = 'create_new_ad.html'
    success_url = '/adboard/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        # Process image and video forms
        if form.cleaned_data['image']:
            Image.objects.create(ad=self.object, is_main=True, image=form.cleaned_data['image'])

        if form.cleaned_data['video']:
            Video.objects.create(ad=self.object, video=form.cleaned_data['video'])

        return response


class AdFeedView(ListView):
    template_name = 'AdBoard.html'
    model = Ad
    ordering = 'date_created'
    context_object_name = 'adboard_with_ads'
    paginate_by = 6


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        img_list = {}
        images = Image.objects.filter(is_main=True)
        for image in images:
            img_list[image.ad.id] = image.image.url
        ads_total = Ad.objects.filter(status='TR').count()
        context['img_list'] = img_list
        context['ads_total'] = ads_total
        return context

class AdDetailView(DetailView):

    model = Ad
    template_name = 'Ad.html'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ad_instance = self.object
        try:
            image = Image.objects.get(is_main=True, ad=ad_instance.id)
            context['image'] = image.image.url
        except:
            context['image'] = None

        try:
            video = Video.objects.get(ad=ad_instance.id)
            context['video'] = video.video
        except:
            context['image'] = None

        return context


class AdUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Ad
    template_name = 'update_ad.html'
    context_object_name = 'ad'
    form_class = AdCreationForm


    def get_object(self, queryset=None):
        ad_id = self.kwargs['pk']
        return get_object_or_404(Ad, id=ad_id)

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        # Process image and video forms
        if form.cleaned_data['image']:
            previous_images = Image.objects.filter(ad=self.object)
            for prev_image in previous_images:
                prev_image.is_main=False
                prev_image.save()
            Image.objects.create(ad=self.object, is_main=True, image=form.cleaned_data['image'])


        if form.cleaned_data['video']:
            Video.objects.create(ad=self.object, video=form.cleaned_data['video'])

        return response


class AdDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Ad
    template_name = 'delete_ad.html'
    context_object_name = 'ad'
    success_url = reverse_lazy('adboard:ad_feed_view')

    def get_object(self, queryset=None):
        ad_id = self.kwargs['pk']
        return get_object_or_404(Ad, id=ad_id)

def ad_views_counter(request):
    ad_id = request.GET.get('ad_id')
    ad = Ad.objects.get(id=ad_id)
    ad.views +=1
    ad.save()

    detail_url = reverse('adboard:detail_ad_view', kwargs={'pk': ad_id})

    return redirect(detail_url)

