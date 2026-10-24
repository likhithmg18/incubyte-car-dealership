
from rest_framework import serializers

from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            'id',
            'make',
            'model',
            'category',
            'price',
            'quantity',
        ]

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError(
                'Quantity cannot be negative.'
            )
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'Price must be greater than zero.'
            )
        return value
