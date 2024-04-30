from django.urls import path
from .views import LoginAPIView, VendorListCreateAPIView, VendorDetailAPIView, PurchaseOrderListCreateAPIView, PurchaseOrderDetailAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='api_login'),
    path('vendors/', VendorListCreateAPIView.as_view(), name='vendor-list-create'),
    path('vendors/<int:vendor_id>/', VendorDetailAPIView.as_view(), name='vendor-detail'),
    path('purchase_orders/', PurchaseOrderListCreateAPIView.as_view(), name='purchase-orders-list-create'),
    path('purchase_orders/<int:po_id>/', PurchaseOrderDetailAPIView.as_view(), name='purchase-order-detail'),
]
