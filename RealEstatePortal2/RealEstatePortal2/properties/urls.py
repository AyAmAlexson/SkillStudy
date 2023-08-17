from django.urls import path
from .views import ResPropertiesList, ResPropertiesDetail, ResPropertyUpdate, ResPropertyDelete, ResPropertiesSearch
from .views import ResPropertyCreateResidential, ResPropertyCreateSales, ResPropertyCreateCommercial

app_name = 'properties'

urlpatterns = [
    path('', ResPropertiesList.as_view(), name='properties_list'),
    path('search/', ResPropertiesSearch.as_view(), name='property_search'),
    path('<str:ref_oct>/', ResPropertiesDetail.as_view(), name='property_details'),
    path('residential/create/', ResPropertyCreateResidential.as_view(), name='property_create'),
    path('sales/create/', ResPropertyCreateSales.as_view(), name='property_create'),
    path('commercial/create/', ResPropertyCreateCommercial.as_view(), name='property_create'),
    path('<str:ref_oct>/update/', ResPropertyUpdate.as_view(), name='property_update'),
    path('<str:ref_oct>/delete/', ResPropertyDelete.as_view(), name='property_delete'),

]