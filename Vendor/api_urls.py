from django.urls import path
from .views import (
    LoginAPIView, 
    VendorListCreateAPIView, 
    VendorDetailAPIView, 
    PurchaseOrderListCreateAPIView, 
    PurchaseOrderDetailAPIView, 
    VendorPerformanceAPIView, 
    PurchaseOrderAcknowledgeAPIView
)

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='api_login'),
    # Vendor Profile Management URLs
    path('vendors/', VendorListCreateAPIView.as_view(), name='vendor-list-create'),
    path('vendors/<int:vendor_id>/', VendorDetailAPIView.as_view(), name='vendor-detail'),
    # Purchase Order Management URLs
    path('purchase_orders/', PurchaseOrderListCreateAPIView.as_view(), name='purchase-orders-list-create'),
    path('purchase_orders/<int:po_id>/', PurchaseOrderDetailAPIView.as_view(), name='purchase-order-detail'),
    # Vendor Performance URL
    path('vendors/<int:vendor_id>/performance/', VendorPerformanceAPIView.as_view(), name='vendor-performance'),
    path('purchase_orders/<int:po_id>/acknowledge/', PurchaseOrderAcknowledgeAPIView.as_view(), name='purchase-order-acknowledge'),
]
