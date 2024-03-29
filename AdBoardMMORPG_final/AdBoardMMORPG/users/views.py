
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View

class AccountDetailView(UserPassesTestMixin, DetailView):
    model = CustomUser
    template_name = 'account_details.html'
    context_object_name = 'account_details'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def test_func(self):
        return self.request.user == self.get_object()

    def get_object(self):
        return self.request.user


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account_instance = self.object
        groups = account_instance.groups.all()
        #subscriptions = account_instance.subscriptions.all()
        context['groups'] = groups
        #context['subscriptions'] = subscriptions
        #context['is_not_agent'] = not self.request.user.groups.filter(name='agents').exists()
        #context['is_not_owner'] = not self.request.user.groups.filter(name='owners').exists()
        #context['is_not_client'] = not self.request.user.groups.filter(name='clients').exists()
        #context['is_not_manager'] = not self.request.user.groups.filter(name='managers').exists()
        return context
