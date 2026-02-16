from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import DeliveryProfile
from .serializers import DeliveryProfileSerializer
from orders.models import Order
from orders.serializers import OrderSerializer

class DeliveryStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, _ = DeliveryProfile.objects.get_or_create(user=request.user)
        return Response(DeliveryProfileSerializer(profile).data)

    def post(self, request):
        profile, _ = DeliveryProfile.objects.get_or_create(user=request.user)
        profile.is_available = request.data.get('is_available', profile.is_available)
        profile.current_location = request.data.get('current_location', profile.current_location)
        profile.save()
        return Response(DeliveryProfileSerializer(profile).data)

class AvailableOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Logic to return orders ready for pickup and nearby (mock proximity)
        return Order.objects.filter(status='PREPARING', delivery_partner__isnull=True)

class AcceptOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, delivery_partner__isnull=True)
        order.delivery_partner = request.user
        order.status = 'PICKED_UP' # Simplified flow
        order.save()
        return Response(OrderSerializer(order).data)
