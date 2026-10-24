
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)

    if request.method == 'GET':
        serializer = VehicleSerializer(vehicle)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = VehicleSerializer(
            vehicle,
            data=request.data,
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Only administrators can delete vehicles.
    if not request.user.is_staff:
        return Response(
            {'detail': 'Only administrators can delete vehicles.'},
            status=status.HTTP_403_FORBIDDEN,
        )

    vehicle.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def purchase_vehicle(request, pk):
    with transaction.atomic():
        updated = Vehicle.objects.filter(
            pk=pk,
            quantity__gt=0,
        ).update(
            quantity=F('quantity') - 1,
        )

        if updated == 0:
            # Return 404 if the vehicle does not exist.
            get_object_or_404(Vehicle, pk=pk)

            # The vehicle exists but has no stock.
            return Response(
                {'detail': 'Vehicle is out of stock.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        vehicle = get_object_or_404(Vehicle, pk=pk)

    serializer = VehicleSerializer(vehicle)
    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
    )


@api_view(['POST'])
def restock_vehicle(request, pk):
    # Only administrators can restock vehicles.
    if not request.user.is_staff:
        return Response(
            {'detail': 'Only administrators can restock vehicles.'},
            status=status.HTTP_403_FORBIDDEN,
        )

    quantity = request.data.get('quantity')

    if quantity is None:
        return Response(
            {'detail': 'Quantity is required.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Reject booleans and non-integer values.
    if isinstance(quantity, bool):
        return Response(
            {'detail': 'Quantity must be a positive integer.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        parsed_quantity = int(quantity)
    except (TypeError, ValueError):
        return Response(
            {'detail': 'Quantity must be a positive integer.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if (
        str(parsed_quantity) != str(quantity).strip()
        or parsed_quantity <= 0
    ):
        return Response(
            {'detail': 'Quantity must be a positive integer.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    with transaction.atomic():
        updated = Vehicle.objects.filter(pk=pk).update(
            quantity=F('quantity') + parsed_quantity,
        )

        if updated == 0:
            get_object_or_404(Vehicle, pk=pk)

        vehicle = get_object_or_404(Vehicle, pk=pk)

    serializer = VehicleSerializer(vehicle)
    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
    )
