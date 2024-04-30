from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import VendorSerializer, PurchaseOrderSerializer
from rest_framework.permissions import IsAuthenticated

## Models Imports
from .models import Vendor, PurchaseOrder

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