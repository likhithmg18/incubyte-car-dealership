
from rest_framework.test import APITestCase
from rest_framework import status


class VehicleListAPITests(APITestCase):
    def test_get_vehicles_returns_successful_response(self):
        response = self.client.get('/api/vehicles/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_get_vehicles_returns_existing_vehicle(self):
        # This test expects the API to return vehicle data from the database.
        response = self.client.get('/api/vehicles/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['make'], 'Toyota')
        self.assertEqual(response.data[0]['model'], 'Corolla')
