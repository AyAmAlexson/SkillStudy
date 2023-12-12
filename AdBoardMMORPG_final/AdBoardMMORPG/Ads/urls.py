from django.urls import path
from .views import AdCreateView, AdFeedView, AdDetailView, AdUpdateView, AdDeleteView, ad_views_counter


app_name = 'adboard'

urlpatterns = [
    path('', AdFeedView.as_view(), name='ad_feed_view'),
    path('ad/create/', AdCreateView.as_view(), name='create_ad_view'),
    path('ad/<int:pk>/', AdDetailView.as_view(), name='detail_ad_view'),
    path('ad/views_inc/', ad_views_counter, name='ad_views_counter'),
    path('ad/<int:pk>/update/', AdUpdateView.as_view(), name='update_ad_view'),
    path('ad/<int:pk>/delete/', AdDeleteView.as_view(), name='delete_ad_view'),
]
