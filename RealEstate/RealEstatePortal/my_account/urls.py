from django.urls import path
from .views import AccountDetails

urlpatterns = [
    path('', AccountDetails.as_view()),
]
