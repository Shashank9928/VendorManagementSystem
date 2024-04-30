from rest_framework import serializers
from .models import Vendor

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'contact_details', 'address', 'vendor_code']

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
