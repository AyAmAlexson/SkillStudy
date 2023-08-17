from django.urls import path
from .views import PropertyEnquiryView

app_name = 'contactus'

urlpatterns = [
    path('property_enquiry/', PropertyEnquiryView.as_view(), name='property_enquiry'),
]