from django.urls import path
from .views import become_agent,become_owner,become_client, AccountDetailView, CategorySubscribe

app_name = 'users'

urlpatterns = [
    path('become_owner/', become_owner, name = 'become_owner'),
    path('become_client/', become_client, name = 'become_client'),
    path('become_agent/', become_agent, name = 'become_agent'),
    path('my_account/', AccountDetailView.as_view(), name='account_details'),
    path('category_subscribe/', CategorySubscribe.as_view(), name='category_subscribe')
]

