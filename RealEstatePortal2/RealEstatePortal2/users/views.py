from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


@login_required
def become_owner(request):
    user = request.user
    owners_group = Group.objects.get(name='owners')
    if not request.user.groups.filter(name='owners').exists():
        owners_group.user_set.add(user)
    return redirect('/property/')

@login_required
def become_client(request):
    user = request.user
    owners_group = Group.objects.get(name='clients')
    if not request.user.groups.filter(name='clients').exists():
        owners_group.user_set.add(user)
    return redirect('/property/')

@login_required
def become_agent(request):
    user = request.user
    owners_group = Group.objects.get(name='agents')
    if not request.user.groups.filter(name='agents').exists():
        owners_group.user_set.add(user)
    return redirect('/property/')


