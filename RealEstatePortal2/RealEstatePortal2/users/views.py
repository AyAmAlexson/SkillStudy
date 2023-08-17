from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import CustomUser, Subscriptions, CustomUser_Subscriptions
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View

from django.core.exceptions import ObjectDoesNotExist
from properties.misc import PROP_DIVISION_REFERENCE

from django.core.mail import send_mail
from django.core.mail import mail_admins
from RealEstatePortal2.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

@login_required
def become_owner(request):
    user = request.user
    owners_group = Group.objects.get(name='owners')
    if not request.user.groups.filter(name='owners').exists():
        owners_group.user_set.add(user)
    return redirect('users:account_details')

@login_required
def become_client(request):
    user = request.user
    owners_group = Group.objects.get(name='clients')
    if not request.user.groups.filter(name='clients').exists():
        owners_group.user_set.add(user)
    return redirect('users:account_details')

@login_required
def become_agent(request):
    user = request.user
    owners_group = Group.objects.get(name='agents')
    if not request.user.groups.filter(name='agents').exists():
        owners_group.user_set.add(user)
    return redirect('users:account_details')

class CategorySubscribe(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        prop_division = request.GET.get('prop_division', None)
        print(prop_division)
        self.set_subscription(user,prop_division,request)
        return redirect('properties:properties_list')

    def set_subscription(self,user,category,request):
        customuser = CustomUser.objects.get(id=user.id)
        subs_count_before = customuser.subscriptions.count()
        try:
            subscription = Subscriptions.objects.get(
                sub_category=category,
                sub_area='',
                sub_min_price=0,
                sub_max_price=None,
                sub_min_bedrooms = 0,
                sub_max_bedrooms=None,
            )
            customuser.subscriptions.add(subscription)
            customuser.save()
            print(f'subscription for {category} category added to {user.username} profile')

        except ObjectDoesNotExist:
            subscription=Subscriptions.objects.create(
                sub_category=category,
                sub_area='',
                sub_min_price=0,
                sub_max_price=None,
                sub_min_bedrooms = 0,
                sub_max_bedrooms=None,
            )
            customuser.subscriptions.add(subscription)
            print(f'subscription for {category} category created and added to {user.username} profile')

        subs_count_after = customuser.subscriptions.count()
        if subs_count_before < subs_count_after:
            # получаем наш html
            html_content = render_to_string(
                'emails/new_subscription.html',
                {
                    'subscription': subscription,
                    'customuser': customuser,
                    'PROP_DIVISION_REFERENCE': PROP_DIVISION_REFERENCE,
                    'request' : request
                }
            )

            msg = EmailMultiAlternatives(
                subject=f'QL Exiles: Your subscription was successful',
                body='',
                from_email=EMAIL_HOST_USER,
                to=[f'{customuser.email}']
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html
            msg.send()  # отсылаем
        else:
            pass



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
        subscriptions = account_instance.subscriptions.all()
        context['groups'] = groups
        context['subscriptions'] = subscriptions
        context['is_not_agent'] = not self.request.user.groups.filter(name='agents').exists()
        context['is_not_owner'] = not self.request.user.groups.filter(name='owners').exists()
        context['is_not_client'] = not self.request.user.groups.filter(name='clients').exists()
        context['is_not_manager'] = not self.request.user.groups.filter(name='managers').exists()
        return context
