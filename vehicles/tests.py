from rest_framework.test import APITestCase
from rest_framework import status


class VehicleListAPITests(APITestCase):
    def test_get_vehicles_returns_successful_response(self):
        response = self.client.get('/api/vehicles/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])