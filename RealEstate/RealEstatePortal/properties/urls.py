from django.urls import path
# Импортируем созданное нами представление
from .views import ResPropertiesList, ResPropertiesDetail , ResPropertyUpdate, ResPropertyDelete, ResPropertiesSearch
from .views import ResPropertyCreateResidential, ResPropertyCreateSales, ResPropertyCreateCommercial

urlpatterns = [
    # path — означает путь.
    # В данном случае путь ко всем товарам у нас останется пустым,
    # чуть позже станет ясно почему.
    # Т.к. наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('', ResPropertiesList.as_view(), name='resproperties_list'),
    path('<int:pk>', ResPropertiesDetail.as_view(), name='resproperty_details'),
    path('residential/create/', ResPropertyCreateResidential.as_view(), name='resproperty_create'),
    path('sales/create/', ResPropertyCreateSales.as_view(), name='resproperty_create'),
    path('commercial/create/', ResPropertyCreateCommercial.as_view(), name='resproperty_create'),
    path('<int:pk>/update/', ResPropertyUpdate.as_view(), name='resproperty_update'),
    path('<int:pk>/delete/', ResPropertyDelete.as_view(), name='resproperty_delete'),
    path('search/', ResPropertiesSearch.as_view(), name='resproperty_search'),
]