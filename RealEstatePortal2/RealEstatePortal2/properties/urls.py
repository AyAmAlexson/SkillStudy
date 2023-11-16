from django.urls import path
from .views import ResPropertiesList, ResPropertiesDetail, ResPropertyUpdate, ResPropertyDelete, ResPropertiesSearch
from .views import ResPropertyCreateResidential, ResPropertyCreateSales, ResPropertyCreateCommercial
from django.views.decorators.cache import cache_page

app_name = 'properties'

urlpatterns = [
    # path('', cache_page(60*5)(ResPropertiesList.as_view()), name='properties_list'), # вариант с кешированием
    path('', ResPropertiesList.as_view(), name='properties_list'), # вариант без кеширования
    path('search/', ResPropertiesSearch.as_view(), name='property_search'),
    path('<str:ref_oct>/', ResPropertiesDetail.as_view(), name='property_details'),
    path('residential/create/', ResPropertyCreateResidential.as_view(), name='property_create'),
    path('sales/create/', ResPropertyCreateSales.as_view(), name='property_create'),
    path('commercial/create/', ResPropertyCreateCommercial.as_view(), name='property_create'),
    path('<str:ref_oct>/update/', ResPropertyUpdate.as_view(), name='property_update'),
    path('<str:ref_oct>/delete/', ResPropertyDelete.as_view(), name='property_delete'),
]