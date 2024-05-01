from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from .serializers import VendorSerializer, PurchaseOrderSerializer
from rest_framework.permissions import IsAuthenticated

#### Calculation Imports
from django.utils import timezone
from django.db.models import Avg, F, ExpressionWrapper, DurationField
from django.db.models.signals import post_save
from django.dispatch import receiver

#### Models Imports
from .models import Vendor, PurchaseOrder, HistoricalPerformance

class LoginAPIView(APIView):
    # Allow any user (authenticated or not) to access this view
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        # Basic input validation
        if not username or not password:
            return Response({"error": "Both username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def get(self, request, *args, **kwargs):
        return Response({"error": "GET method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def put(self, request, *args, **kwargs):
        return Response({"error": "PUT method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, *args, **kwargs):
        return Response({"error": "DELETE method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
    
class VendorListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class VendorDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, vendor_id):
        try:
            return Vendor.objects.get(pk=vendor_id)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, vendor_id):
        vendor = self.get_object(vendor_id)
        if isinstance(vendor, Response):
            return vendor
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    def put(self, request, vendor_id):
        vendor = self.get_object(vendor_id)
        if isinstance(vendor, Response):
            return vendor
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, vendor_id):
        vendor = self.get_object(vendor_id)
        if isinstance(vendor, Response):
            return vendor
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PurchaseOrderListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        vendor_id = request.query_params.get('vendor_id', None)
        if vendor_id:
            purchase_orders = PurchaseOrder.objects.filter(vendor__id=vendor_id)
        else:
            purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseOrderDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, po_id):
        try:
            return PurchaseOrder.objects.get(pk=po_id)
        except PurchaseOrder.DoesNotExist:
            return Response({'error': 'Purchase order not found'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, po_id):
        purchase_order = self.get_object(po_id)
        if isinstance(purchase_order, Response):
            return purchase_order
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)

    def put(self, request, po_id):
        purchase_order = self.get_object(po_id)
        if isinstance(purchase_order, Response):
            return purchase_order
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, po_id):
        purchase_order = self.get_object(po_id)
        if isinstance(purchase_order, Response):
            return purchase_order
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
def calculate_on_time_delivery_rate(vendor):
    """
    Calculate and update the on-time delivery rate for a vendor.
    """
    total_delivered_on_time = PurchaseOrder.objects.filter(vendor=vendor, status='completed', delivery_date__lte=F('order_date')).count()
    total_completed = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
    if total_completed > 0:
        on_time_delivery_rate = (total_delivered_on_time / total_completed) * 100
        vendor.on_time_delivery_rate = on_time_delivery_rate
        vendor.save()

def calculate_quality_rating_average(vendor):
    """
    Calculate and update the average quality rating for completed POs of a vendor.
    """
    quality_ratings = PurchaseOrder.objects.filter(
        vendor=vendor, 
        status='completed', 
        quality_rating__isnull=False
    ).aggregate(Avg('quality_rating'))
    vendor.quality_rating_avg = quality_ratings['quality_rating__avg'] or 0
    vendor.save()

def calculate_average_response_time(vendor):
    """
    Calculate and update the average response time for acknowledged POs of a vendor.
    """
    response_times = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False).annotate(
        response_time=ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=DurationField())
    ).aggregate(avg_response_time=Avg('response_time'))
    if response_times['avg_response_time']:
        vendor.average_response_time = response_times['avg_response_time'].total_seconds() / 3600
        vendor.save()

def calculate_fulfillment_rate(vendor):
    """
    Calculate and update the fulfillment rate for a vendor.
    """
    total_fulfilled = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
    total_orders = PurchaseOrder.objects.filter(vendor=vendor).count()
    if total_orders > 0:
        fulfillment_rate = (total_fulfilled / total_orders) * 100
        vendor.fulfillment_rate = fulfillment_rate
        vendor.save()

    
@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics(sender, instance, created, **kwargs):
    """
    Signal to update vendor metrics whenever a Purchase Order is saved.
    """
    if instance.status == 'completed':
        # On-Time Delivery Rate and Quality Rating Average calculation
        calculate_on_time_delivery_rate(instance.vendor)
        if instance.quality_rating is not None:
            calculate_quality_rating_average(instance.vendor)

    if instance.acknowledgment_date:
        # Average Response Time calculation
        calculate_average_response_time(instance.vendor)

    # Fulfillment Rate is updated upon any status change
    calculate_fulfillment_rate(instance.vendor)
    update_or_create_daily_performance(instance.vendor.id)
    
def update_or_create_daily_performance(vendor_id):
    # Check if the vendor exists
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        print("Vendor not found")
        return

    # Determine today's date
    today = timezone.localdate()

    # Fetch today's performance record, if it exists
    historical_record, created = HistoricalPerformance.objects.get_or_create(
        vendor=vendor,
        date=today,
        defaults={
            'on_time_delivery_rate': 0,
            'quality_rating_avg': 0,
            'average_response_time': 0,
            'fulfillment_rate': 0,
        }
    )

    # Calculate the metrics
    orders = PurchaseOrder.objects.filter(vendor=vendor, order_date__date=today)
    total_completed = orders.filter(status='completed').count()

    if total_completed > 0:
        on_time_delivery_rate = 100 * orders.filter(delivery_date__lte=F('order_date')).count() / total_completed
        quality_rating_avg = orders.aggregate(avg_quality=Avg('quality_rating'))['avg_quality'] or 0

        response_times = orders.filter(acknowledgment_date__isnull=False).annotate(
            response_time=ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=DurationField())
        ).aggregate(avg_response_time=Avg('response_time'))
        average_response_time = response_times['avg_response_time'].total_seconds() / 3600 if response_times['avg_response_time'] else 0

        fulfillment_rate = 100 * orders.filter(vendor=vendor,status="completed").count() / total_completed

        # Update the historical record with new data
        historical_record.on_time_delivery_rate = on_time_delivery_rate
        historical_record.quality_rating_avg = quality_rating_avg
        historical_record.average_response_time = average_response_time
        historical_record.fulfillment_rate = fulfillment_rate
        historical_record.save()
    else:
        print("No completed orders found for today")
        
        
class VendorPerformanceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        today = timezone.localdate()
        performance = HistoricalPerformance.objects.filter(vendor=vendor, date=today).first()

        if performance:
            data = {
                'on_time_delivery_rate': performance.on_time_delivery_rate,
                'quality_rating_avg': performance.quality_rating_avg,
                'average_response_time': performance.average_response_time,
                'fulfillment_rate': performance.fulfillment_rate
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No performance data available for today.'}, status=status.HTTP_404_NOT_FOUND)
        
        
class PurchaseOrderAcknowledgeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, po_id):
        purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)

        if not purchase_order.acknowledgment_date:
            purchase_order.acknowledgment_date = timezone.now()
            purchase_order.save()
            return Response({'message': 'Purchase order acknowledged successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Purchase order already acknowledged.'}, status=status.HTTP_400_BAD_REQUEST)