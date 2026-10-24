
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from vehicles.models import Vehicle


class VehicleListAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass123!',
        )
        self.client.force_authenticate(user=self.user)

    def test_get_vehicles_returns_successful_response(self):
        response = self.client.get('/api/vehicles/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

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
        self.assertEqual(response.data[0]['model'], 'Corolla')
        self.assertEqual(response.data[0]['category'], 'Sedan')
        self.assertEqual(response.data[0]['quantity'], 3)

    def test_create_vehicle(self):
        payload = {
            'make': 'Honda',
            'model': 'Civic',
            'category': 'Sedan',
            'price': '28000.00',
            'quantity': 5,
        }

        response = self.client.post(
            '/api/vehicles/',
            payload,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vehicle.objects.count(), 1)
        self.assertEqual(Vehicle.objects.get().make, 'Honda')

    def test_create_vehicle_rejects_negative_quantity(self):
        payload = {
            'make': 'Honda',
            'model': 'Civic',
            'category': 'Sedan',
            'price': '28000.00',
            'quantity': -1,
        }

        response = self.client.post(
            '/api/vehicles/',
            payload,
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
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
            quantity=5,
        )

        response = self.client.get(
            '/api/vehicles/search/',
            {'make': 'Toyota'},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['make'], 'Toyota')
        self.assertEqual(response.data[0]['model'], 'Corolla')

    def test_update_vehicle(self):
        vehicle = Vehicle.objects.create(
            make='Toyota',
            model='Corolla',
            category='Sedan',
            price=25000,
            quantity=3,
        )

        payload = {
            'make': 'Toyota',
            'model': 'Camry',
            'category': 'Sedan',
            'price': '30000.00',
            'quantity': 4,
        }

        response = self.client.put(
            f'/api/vehicles/{vehicle.id}/',
            payload,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        vehicle.refresh_from_db()
        self.assertEqual(vehicle.model, 'Camry')
        self.assertEqual(vehicle.price, 30000)
        self.assertEqual(vehicle.quantity, 4)

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
        admin_user = User.objects.create_user(
            username='adminuser',
            password='AdminPass123!',
            is_staff=True,
        )

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

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

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
        admin_user = User.objects.create_user(
            username='restockadmin',
            password='AdminPass123!',
            is_staff=True,
        )

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

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        vehicle.refresh_from_db()
        self.assertEqual(vehicle.quantity, 8)