from django.urls import path
from .views import db_update

urlpatterns = [
    path('from_QL_public/', db_update, name = 'QL_public_update'),
]