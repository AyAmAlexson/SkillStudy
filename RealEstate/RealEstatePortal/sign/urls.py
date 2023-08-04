from django.urls import path
from .views import become_owner, become_client, become_agent
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('login/',
         LoginView.as_view(template_name = 'login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name = 'logout.html'),
         name='logout'),
    path('become_owner/', become_owner, name = 'become_owner'),
    path('become_client/', become_client, name = 'become_client'),
    path('become_agent/', become_agent, name = 'become_agent'),
]