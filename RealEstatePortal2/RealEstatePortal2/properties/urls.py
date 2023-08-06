from django.urls import path
from .views import ResPropertiesList, ResPropertiesDetail, ResPropertyUpdate, ResPropertyDelete, ResPropertiesSearch
from .views import ResPropertyCreateResidential, ResPropertyCreateSales, ResPropertyCreateCommercial

urlpatterns = [
    path('', ResPropertiesList.as_view(), name='properties_list'),
    path('<int:pk>', ResPropertiesDetail.as_view(), name='property_details'),
    path('residential/create/', ResPropertyCreateResidential.as_view(), name='property_create'),
    path('sales/create/', ResPropertyCreateSales.as_view(), name='property_create'),
    path('commercial/create/', ResPropertyCreateCommercial.as_view(), name='property_create'),
    path('<int:pk>/update/', ResPropertyUpdate.as_view(), name='property_update'),
    path('<int:pk>/delete/', ResPropertyDelete.as_view(), name='property_delete'),
    path('search/', ResPropertiesSearch.as_view(), name='property_search'),
]