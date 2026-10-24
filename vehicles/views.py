
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Vehicle


def serialize_vehicle(vehicle):
    return {
        'id': vehicle.id,
        'make': vehicle.make,
        'model': vehicle.model,
        'category': vehicle.category,
        'price': str(vehicle.price),
        'quantity': vehicle.quantity,
    }


@api_view(['GET', 'POST'])
def vehicle_list(request):
    if request.method == 'GET':
        vehicles = Vehicle.objects.all()
        data = [serialize_vehicle(vehicle) for vehicle in vehicles]
        return Response(data)

    vehicle = Vehicle.objects.create(
        make=request.data['make'],
        model=request.data['model'],
        category=request.data['category'],
        price=request.data['price'],
        quantity=request.data['quantity'],
    )

    return Response(
        serialize_vehicle(vehicle),
        status=status.HTTP_201_CREATED,
    )
