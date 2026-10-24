
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Vehicle
from .serializers import VehicleSerializer


@api_view(['GET', 'POST'])
def vehicle_list(request):
    if request.method == 'GET':
        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)

    serializer = VehicleSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(['GET'])
def vehicle_search(request):
    vehicles = Vehicle.objects.all()

    make = request.query_params.get('make')
    model = request.query_params.get('model')
    category = request.query_params.get('category')
    min_price = request.query_params.get('min_price')
    max_price = request.query_params.get('max_price')

    if make:
        vehicles = vehicles.filter(make__icontains=make)

    if model:
        vehicles = vehicles.filter(model__icontains=model)

    if category:
        vehicles = vehicles.filter(category__icontains=category)

    if min_price:
        vehicles = vehicles.filter(price__gte=min_price)

    if max_price:
        vehicles = vehicles.filter(price__lte=max_price)

    serializer = VehicleSerializer(vehicles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
