from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from models import CustomUser

@login_required
def become_owner(request):
    user = request.user
    owners_group = Group.objects.get(name='owners')
    if not request.user.groups.filter(name='owners').exists():
        owners_group.user_set.add(user)
    return redirect('/resproperties/')

@login_required
def become_client(request):
    user = request.user
    owners_group = Group.objects.get(name='clients')
    if not request.user.groups.filter(name='clients').exists():
        owners_group.user_set.add(user)
    return redirect('/resproperties/')

@login_required
def become_agent(request):
    user = request.user
    owners_group = Group.objects.get(name='agents_residential')
    if not request.user.groups.filter(name='agents_residential').exists():
        owners_group.user_set.add(user)
    owners_group = Group.objects.get(name='agents_commercial')
    if not request.user.groups.filter(name='agents_commercial').exists():
        owners_group.user_set.add(user)
    owners_group = Group.objects.get(name='agents_sales')
    if not request.user.groups.filter(name='agents_sales').exists():
        owners_group.user_set.add(user)

    return redirect('/resproperties/')