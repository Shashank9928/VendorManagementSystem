from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from .models import Vendor, PurchaseOrder, HistoricalPerformance
import datetime
from django.utils import timezone

class AuthenticationTestCase(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.login_url = reverse('api_login')

    def test_successful_login(self):
        """
        Ensure we can successfully log in a user and receive a token.
        """
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        token = Token.objects.get(user=self.user)
        self.assertEqual(response.data['token'], token.key)

    def test_incorrect_credentials(self):
        """
        Ensure login fails with incorrect credentials.
        """
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid Credentials')

    def test_missing_credentials(self):
        """
        Ensure that login request fails if required fields are missing.
        """
        data = {'username': 'testuser'}
        response = self.client.post(self.login_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Both username and password are required.')

    def test_unsupported_methods(self):
        """
        Ensure that GET, PUT, and DELETE methods are not allowed.
        """
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(self.login_url, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete(self.login_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        
class VendorListCreateAPITests(APITestCase):

    def setUp(self):
        # Create a user and set up token authentication
        self.user = User.objects.create_user(username='user', password='password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # URL for creating and listing vendors
        self.url = reverse('vendor-list-create')

        # Create sample vendors
        Vendor.objects.create(name="Vendor A", contact_details="Contact A", address="Address A", vendor_code="CodeA")
        Vendor.objects.create(name="Vendor B", contact_details="Contact B", address="Address B", vendor_code="CodeB")

    def test_list_vendors(self):
        """
        Ensure we can list all vendors.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Check that all vendors are listed

    def test_create_vendor(self):
        """
        Ensure we can create a new vendor.
        """
        data = {
            'name': 'Vendor C',
            'contact_details': '12345678901',
            'address': 'Address Address Address Address Address',
            'vendor_code': 'CodeC'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 3)  # Including the initially created vendors
        self.assertEqual(Vendor.objects.get(name='Vendor C').contact_details, '12345678901')

    def test_create_vendor_invalid_data(self):
        """
        Ensure we get an error if the data is invalid.
        """
        data = {'name': ''}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('name' in response.data)  # Error should include a message about the name field

    def test_unauthorized_access(self):
        """
        Ensure unauthorized access is forbidden.
        """
        # Clear the authentication credentials
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
class PurchaseOrderTests(APITestCase):
    def setUp(self):
        # Create a user and token for authentication
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create a vendor
        self.vendor = Vendor.objects.create(name="Vendor1", contact_details="Some details", address="Some address", vendor_code="V001")

        # Create a purchase order
        self.purchase_order = PurchaseOrder.objects.create(
            vendor=self.vendor,
            po_number="PO123",
            order_date=timezone.now(),
            delivery_date=timezone.now() + timezone.timedelta(days=10),
            items='{"item": "widget", "quantity": 10}',
            quantity=10,
            status='pending'
        )
    
    def test_list_vendors(self):
        url = reverse('vendor-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_vendor(self):
        url = reverse('vendor-list-create')
        data = {
            'name': 'New Vendor',
            'contact_details': 'new contact details',
            'address': 'new address',
            'vendor_code': 'V002'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 2)
    def test_list_purchase_orders(self):
        url = reverse('purchase-orders-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_purchase_order(self):
        url = reverse('purchase-orders-list-create')
        data = {
            'vendor': self.vendor.id,
            'po_number': "PO124",
            'order_date': datetime.datetime.now().isoformat(),
            'delivery_date': (datetime.datetime.now() + datetime.timedelta(days=10)).isoformat(),
            'items': '{"item": "widget2", "quantity": 20}',
            'quantity': 20,
            'status': 'pending'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 2)

    def test_retrieve_purchase_order(self):
        url = reverse('purchase-order-detail', kwargs={'po_id': self.purchase_order.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_purchase_order(self):
        url = reverse('purchase-order-detail', kwargs={'po_id': self.purchase_order.id})

        updated_data = {
            'vendor': self.vendor.id,
            'po_number': "PO124",
            'order_date': datetime.datetime.now().isoformat(),
            'delivery_date': (datetime.datetime.now() + datetime.timedelta(days=10)).isoformat(),
            'items': '{"item": "widget2", "quantity": 20}',
            'quantity': 20,
            'status': 'completed'
        }
        
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Reload the data from the database
        self.purchase_order.refresh_from_db()

        # Assert that the status has been updated to 'completed'
        self.assertEqual(self.purchase_order.status, 'completed')


class VendorPurchaseOrderPerformanceTests(APITestCase):
    def setUp(self):
        # User setup
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Vendor setup
        self.vendor = Vendor.objects.create(name="Vendor1", contact_details="Details", address="Address", vendor_code="V100")

        # Purchase orders setup
        for i in range(1, 5):  # Create several to average
            po = PurchaseOrder.objects.create(
                vendor=self.vendor,
                po_number=f"PO12{i}",
                order_date=timezone.now(),
                delivery_date=timezone.now() + timezone.timedelta(days=1),
                issue_date=timezone.now(),
                items=f'{{"item": "widget{i}", "quantity": {i * 10}}}',
                quantity=i * 10,
                status='completed',
                quality_rating=4.0 + i * 0.1
            )
            if i == 1:  # Assign one order for specific tests
                self.purchase_order = po

        # Historical performance setup
        historical_performance, created = HistoricalPerformance.objects.get_or_create(
            vendor=self.vendor,
            date=timezone.now().date(),
            defaults={
                'on_time_delivery_rate': 95.0,
                'quality_rating_avg': 4.25,
                'average_response_time': 2.0,
                'fulfillment_rate': 100.0,
            }
        )
        self.historical_performance = historical_performance

    def test_vendor_performance_retrieval(self):
        url = reverse('vendor-performance', kwargs={'vendor_id': self.vendor.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('on_time_delivery_rate', response.data)
        self.assertEqual(response.data['quality_rating_avg'], 4.25)  # Ensuring the manually set average is tested

    def test_purchase_order_acknowledgment(self):
        url = reverse('purchase-order-acknowledge', kwargs={'po_id': self.purchase_order.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.purchase_order.refresh_from_db()
        self.assertIsNotNone(self.purchase_order.acknowledgment_date)
        self.assertEqual(response.data['message'], 'Purchase order acknowledged successfully.')

    def test_update_historical_performance(self):
        # Manually trigger update to reflect changes
        self.purchase_order.status = 'completed'
        self.purchase_order.quality_rating = 4.5  # Changing quality rating to trigger average calculation
        self.purchase_order.save()
        self.historical_performance.refresh_from_db()
        # Check if fulfillment rate changes as expected based on completion status
        expected_fulfillment_rate = (1 / 1) * 100  # Assuming this PO is the only one considered
        self.assertEqual(self.historical_performance.fulfillment_rate, expected_fulfillment_rate)
