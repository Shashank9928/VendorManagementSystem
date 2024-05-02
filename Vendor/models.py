from django.db import models
from django.utils import  timezone
from django.core.validators import (
    MinLengthValidator, 
    MaxValueValidator, 
    MinValueValidator
    )

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField(validators=[MinLengthValidator(10)])
    address = models.TextField(validators=[MinLengthValidator(10)])
    vendor_code = models.CharField(max_length=100, unique=True)
    on_time_delivery_rate = models.FloatField(
        default=0.0, 
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
        )
    quality_rating_avg = models.FloatField(
        default=0.0, 
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
        )
    average_response_time = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    fulfillment_rate = models.FloatField(
        default=0.0, 
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
        )
    
    def __str__(self):
        return f"{self.name} ({self.vendor_code})"


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(
        Vendor, 
        on_delete=models.CASCADE, related_name='purchase_orders'
        )
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(
        max_length=20, default='pending', 
        choices=[('pending', 'Pending'),('completed', 'Completed'),('canceled', 'Canceled')]
        )
    quality_rating = models.FloatField(
        null=True, 
        blank=True, 
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
        )
    issue_date = models.DateTimeField(default=timezone.now)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PO {self.po_number} - {self.status}"


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(
        Vendor, 
        on_delete=models.CASCADE, 
        related_name='historical_performances'
        )
    date = models.DateField()
    on_time_delivery_rate = models.FloatField(
        default=0.0, 
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
        )
    quality_rating_avg = models.FloatField(
        default=0.0, 
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
        )
    average_response_time = models.FloatField(
        default=0.0, 
        validators=[MinValueValidator(0.0)]
        )
    fulfillment_rate = models.FloatField(
        default=0.0, 
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
        )
    class Meta:
        unique_together = ('vendor', 'date')

    def __str__(self):
        return f"Performance on {self.date.strftime('%Y-%m-%d')} for {self.vendor.name}"
