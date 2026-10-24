
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
