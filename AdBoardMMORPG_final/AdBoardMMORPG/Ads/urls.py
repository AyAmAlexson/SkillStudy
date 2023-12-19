from django.urls import path
from .views import AdCreateView, AdFeedView, AdDetailView, AdUpdateView, AdDeleteView,\
    CreateResponseView, SuccessResponseView, ad_views_counter, AdsSearch


app_name = 'adboard'

urlpatterns = [
    path('', AdFeedView.as_view(), name='ad_feed_view'),
    path('search/', AdsSearch.as_view(), name='ad_search_view'),
    path('ad/create/', AdCreateView.as_view(), name='create_ad_view'),
    path('ad/<int:pk>/', AdDetailView.as_view(), name='detail_ad_view'),
    path('ad/views_inc/', ad_views_counter, name='ad_views_counter'),
    path('ad/<int:pk>/update/', AdUpdateView.as_view(), name='update_ad_view'),
    path('ad/<int:pk>/delete/', AdDeleteView.as_view(), name='delete_ad_view'),
    path('ad/<int:pk>/response/', CreateResponseView.as_view(), name='create_response_view'),
    path('ad/<int:pk>/response/success/', SuccessResponseView.as_view(), name='response_success'),

]
