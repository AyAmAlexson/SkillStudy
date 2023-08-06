from django.urls import path
from .views import become_agent,become_owner,become_client

urlpatterns = [
    path('become_owner/', become_owner, name = 'become_owner'),
    path('become_client/', become_client, name = 'become_client'),
    path('become_agent/', become_agent, name = 'become_agent'),
]

