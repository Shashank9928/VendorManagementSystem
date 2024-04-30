from django.contrib import admin
from .models import Vendor, PurchaseOrder, HistoricalPerformance


class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor_code', 'contact_details', 'address')
    search_fields = ('name', 'vendor_code')


class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = (
        'po_number', 'vendor', 'order_date', 'delivery_date', 'status'
    )
    list_filter = ('status', 'order_date')
    search_fields = ('po_number', 'vendor__name')


class HistoricalPerformanceAdmin(admin.ModelAdmin):
    list_display = (
        'vendor', 'date', 'on_time_delivery_rate', 'quality_rating_avg',
        'average_response_time', 'fulfillment_rate'
    )
    list_filter = ('date',)
    search_fields = ('vendor__name',)


admin.site.register(Vendor, VendorAdmin)
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(HistoricalPerformance, HistoricalPerformanceAdmin)