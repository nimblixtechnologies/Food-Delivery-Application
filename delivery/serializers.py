from rest_framework import serializers
from .models import DeliveryProfile
from orders.serializers import OrderSerializer

class DeliveryProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryProfile
        fields = ['is_available', 'current_location']
