
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Vehicle


@api_view(['GET'])
def vehicle_list(request):
    vehicles = Vehicle.objects.all()

    data = [
        {
            'id': vehicle.id,
            'make': vehicle.make,
            'model': vehicle.model,
            'category': vehicle.category,
            'price': str(vehicle.price),
            'quantity': vehicle.quantity,
        }
        for vehicle in vehicles
    ]

    return Response(data)
