from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'contact_details', 'address', 'vendor_code']

    def validate_vendor_code(self, value):
        """
        Check that the vendor code is unique and follows a specific format.
        """
        if not value.isalnum():
            raise serializers.ValidationError("Vendor code must be alphanumeric.")
        if Vendor.objects.filter(vendor_code=value).exists():
            raise serializers.ValidationError("Vendor code must be unique.")
        return value

    def validate_contact_details(self, value):
        """
        Check that contact details are provided.
        """
        if not value.strip():
            raise serializers.ValidationError("Contact details must not be empty.")
        return value

    def validate_address(self, value):
        """
        Check that the address is not empty.
        """
        if not value.strip():
            raise serializers.ValidationError("Address must not be empty.")
        return value
    
    def create(self, validated_data):
        """
        Create and return a new `Vendor` instance, given the validated data.
        """
        return Vendor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Vendor` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.contact_details = validated_data.get('contact_details', instance.contact_details)
        instance.address = validated_data.get('address', instance.address)
        instance.vendor_code = validated_data.get('vendor_code', instance.vendor_code)
        instance.save()
        return instance
    
class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['id', 'po_number', 'vendor','issue_date', 'order_date', 'delivery_date', 'items', 'quantity', 'status']
    
    def validate(self, data):
        """
        Add custom validation for the PurchaseOrder data.
        """
        # Ensure delivery date is after order date
        if 'delivery_date' in data and 'order_date' in data:
            if data['delivery_date'] < data['order_date']:
                raise serializers.ValidationError("Delivery date must be after order date.")
        
        # Check for status transitions that might not be allowed
        if self.instance and 'status' in data:
            if self.instance.status == 'completed' and data['status'] != 'completed':
                raise serializers.ValidationError("Cannot change status from completed to another status.")

        return data

    def validate_vendor(self, value):
        """
        Validate that the vendor ID exists.
        """
        if not Vendor.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Vendor with this ID does not exist.")
        return value

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'