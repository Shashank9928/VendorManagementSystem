from django.urls import path
from .views import LoginAPIView, VendorListCreateAPIView, VendorDetailAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='api_login'),
    path('vendors/', VendorListCreateAPIView.as_view(), name='vendor-list-create'),
    path('vendors/<int:vendor_id>/', VendorDetailAPIView.as_view(), name='vendor-detail'),
]
