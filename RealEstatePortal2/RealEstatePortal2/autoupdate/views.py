from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from properties.models import ResProperties, Owners, Agents
from data_parser import data_parser
#from core.views import base_view

@login_required
def db_update(request):
    user = request.user
    _data_parser = data_parser()
    p = _data_parser.get_property()
    ResProperties.objects.create(ref=p["ref"], prop_type=p["prop_type"], location=p["prop_location"],
                                 address=" ", _price=p["price"], status=p["status"],
                                 status_valid=p["status"], bedrooms=p["bedrooms"], bathrooms=p["bathrooms"],
                                 prop_description=p["description"],
                                 owner=Owners.objects.get(id=1), added_by=Agents.objects.get(id=user.id))
    return JsonResponse({"success": "True"})


