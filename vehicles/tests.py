
from rest_framework.test import APITestCase
from rest_framework import status

from vehicles.models import Vehicle


class VehicleListAPITests(APITestCase):

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

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
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

        response = self.client.delete(
            f'/api/vehicles/{vehicle.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        self.assertTrue(
            Vehicle.objects.filter(id=vehicle.id).exists()
        )
