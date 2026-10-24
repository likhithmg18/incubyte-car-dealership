
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from vehicles.models import Vehicle


class VehicleListAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass123!',
        )
        self.client.force_authenticate(user=self.user)

    def create_admin(self, username='testadmin'):
        return User.objects.create_user(
            username=username,
            password='AdminPass123!',
            is_staff=True,
        )

    def test_get_vehicles_returns_successful_response(self):
        response = self.client.get('/api/vehicles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_vehicles_returns_existing_vehicle(self):
        Vehicle.objects.create(
            make='Toyota',
            model='Corolla',
            category='Sedan',
            price=25000,
            quantity=3,
        )

        response = self.client.get('/api/vehicles/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['make'], 'Toyota')

    def test_admin_can_create_vehicle(self):
        admin_user = self.create_admin('createadmin')
        self.client.force_authenticate(user=admin_user)

        data = {
            'make': 'Honda',
            'model': 'Civic',
            'category': 'Sedan',
            'price': '28000.00',
            'quantity': 5,
        }

        response = self.client.post(
            '/api/vehicles/',
            data,
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(Vehicle.objects.count(), 1)

    def test_create_vehicle_rejects_negative_quantity(self):
        admin_user = self.create_admin('negativeadmin')
        self.client.force_authenticate(user=admin_user)

        data = {
            'make': 'Honda',
            'model': 'Civic',
            'category': 'Sedan',
            'price': '28000.00',
            'quantity': -1,
        }

        response = self.client.post(
            '/api/vehicles/',
            data,
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertEqual(Vehicle.objects.count(), 0)

    def test_regular_user_cannot_create_vehicle(self):
        data = {
            'make': 'Honda',
            'model': 'Civic',
            'category': 'Sedan',
            'price': '28000.00',
            'quantity': 5,
        }

        response = self.client.post(
            '/api/vehicles/',
            data,
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(Vehicle.objects.count(), 0)

    def test_search_vehicles_by_make(self):
        Vehicle.objects.create(
            make='Toyota',
            model='Corolla',
            category='Sedan',
            price=25000,
            quantity=3,
        )
        Vehicle.objects.create(
            make='Honda',
            model='Civic',
            category='Sedan',
            price=28000,
            quantity=4,
        )

        response = self.client.get(
            '/api/vehicles/search/?make=Toyota'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['make'], 'Toyota')
        self.assertEqual(response.data[0]['model'], 'Corolla')

    def test_admin_can_update_vehicle(self):
        admin_user = self.create_admin('updateadmin')
        self.client.force_authenticate(user=admin_user)

        vehicle = Vehicle.objects.create(
            make='Toyota',
            model='Corolla',
            category='Sedan',
            price=25000,
            quantity=3,
        )

        data = {
            'make': 'Toyota',
            'model': 'Corolla',
            'category': 'Sedan',
            'price': '30000.00',
            'quantity': 4,
        }

        response = self.client.put(
            f'/api/vehicles/{vehicle.id}/',
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        vehicle.refresh_from_db()
        self.assertEqual(vehicle.price, 30000)
        self.assertEqual(vehicle.quantity, 4)

    def test_regular_user_cannot_update_vehicle(self):
        vehicle = Vehicle.objects.create(
            make='Toyota',
            model='Corolla',
            category='Sedan',
            price=25000,
            quantity=3,
        )

        data = {
            'make': 'Toyota',
            'model': 'Corolla',
            'category': 'Sedan',
            'price': '30000.00',
            'quantity': 4,
        }

        response = self.client.put(
            f'/api/vehicles/{vehicle.id}/',
            data,
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        vehicle.refresh_from_db()
        self.assertEqual(vehicle.price, 25000)
        self.assertEqual(vehicle.quantity, 3)

    def test_delete_vehicle_requires_authentication(self):
        vehicle = Vehicle.objects.create(
            make='Toyota',
            model='Corolla',
            category='Sedan',
            price=25000,
            quantity=3,
        )

        anonymous_client = APIClient()
        response = anonymous_client.delete(
            f'/api/vehicles/{vehicle.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        self.assertTrue(
            Vehicle.objects.filter(id=vehicle.id).exists()
        )

    def test_regular_user_cannot_delete_vehicle(self):
        vehicle = Vehicle.objects.create(
            make='Toyota',
            model='Corolla',
            category='Sedan',
            price=25000,
            quantity=3,
        )

        response = self.client.delete(
            f'/api/vehicles/{vehicle.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertTrue(
            Vehicle.objects.filter(id=vehicle.id).exists()
        )

    def test_admin_can_delete_vehicle(self):
        admin_user = self.create_admin('deleteadmin')

        vehicle = Vehicle.objects.create(
            make='Toyota',
            model='Corolla',
            category='Sedan',
            price=25000,
            quantity=3,
        )

        self.client.force_authenticate(user=admin_user)

        response = self.client.delete(
            f'/api/vehicles/{vehicle.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Vehicle.objects.filter(id=vehicle.id).exists()
        )

    def test_purchase_vehicle_reduces_quantity(self):
        vehicle = Vehicle.objects.create(
            make='Toyota',
            model='Corolla',
            category='Sedan',
            price=25000,
            quantity=3,
        )

        response = self.client.post(
            f'/api/vehicles/{vehicle.id}/purchase/'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        vehicle.refresh_from_db()
        self.assertEqual(vehicle.quantity, 2)

    def test_purchase_out_of_stock_vehicle_fails(self):
        vehicle = Vehicle.objects.create(
            make='Toyota',
            model='Corolla',
            category='Sedan',
            price=25000,
            quantity=0,
        )

        response = self.client.post(
            f'/api/vehicles/{vehicle.id}/purchase/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        vehicle.refresh_from_db()
        self.assertEqual(vehicle.quantity, 0)

    def test_regular_user_cannot_restock_vehicle(self):
        vehicle = Vehicle.objects.create(
            make='Toyota',
            model='Corolla',
            category='Sedan',
            price=25000,
            quantity=3,
        )

        response = self.client.post(
            f'/api/vehicles/{vehicle.id}/restock/',
            {'quantity': 5},
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        vehicle.refresh_from_db()
        self.assertEqual(vehicle.quantity, 3)

    def test_admin_can_restock_vehicle(self):
        admin_user = self.create_admin('restockadmin')

        vehicle = Vehicle.objects.create(
            make='Toyota',
            model='Corolla',
            category='Sedan',
            price=25000,
            quantity=3,
        )

        self.client.force_authenticate(user=admin_user)

        response = self.client.post(
            f'/api/vehicles/{vehicle.id}/restock/',
            {'quantity': 5},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        vehicle.refresh_from_db()
        self.assertEqual(vehicle.quantity, 8)

    def test_purchase_does_not_make_quantity_negative(self):
        vehicle = Vehicle.objects.create(
            make='Toyota',
            model='Corolla',
            category='Sedan',
            price=25000,
            quantity=1,
        )

        first_response = self.client.post(
            f'/api/vehicles/{vehicle.id}/purchase/'
        )
        second_response = self.client.post(
            f'/api/vehicles/{vehicle.id}/purchase/'
        )

        self.assertEqual(
            first_response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            second_response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        vehicle.refresh_from_db()
        self.assertEqual(vehicle.quantity, 0)

    def test_anonymous_user_cannot_list_vehicles(self):
        anonymous_client = APIClient()

        response = anonymous_client.get('/api/vehicles/')

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_anonymous_user_cannot_create_vehicle(self):
        anonymous_client = APIClient()

        data = {
            'make': 'Honda',
            'model': 'Civic',
            'category': 'Sedan',
            'price': '28000.00',
            'quantity': 5,
        }

        response = anonymous_client.post(
            '/api/vehicles/',
            data,
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        self.assertEqual(Vehicle.objects.count(), 0)

    def test_anonymous_user_cannot_purchase_vehicle(self):
        vehicle = Vehicle.objects.create(
            make='Toyota',
            model='Camry',
            category='Sedan',
            price=25000,
            quantity=3,
        )

        anonymous_client = APIClient()

        response = anonymous_client.post(
            f'/api/vehicles/{vehicle.id}/purchase/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        vehicle.refresh_from_db()
        self.assertEqual(vehicle.quantity, 3)

    def test_anonymous_user_cannot_search_vehicles(self):
        anonymous_client = APIClient()

        response = anonymous_client.get(
            '/api/vehicles/search/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
