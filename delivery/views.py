from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import DeliveryProfile
from .serializers import DeliveryProfileSerializer
from orders.models import Order
from orders.serializers import OrderSerializer


# ----------------------------
# DELIVERY PROFILE STATUS
# ----------------------------
class DeliveryStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, _ = DeliveryProfile.objects.get_or_create(user=request.user)
        return Response(DeliveryProfileSerializer(profile).data)

    def post(self, request):
        profile, _ = DeliveryProfile.objects.get_or_create(user=request.user)

        profile.is_available = request.data.get("is_available", profile.is_available)
        profile.current_location = request.data.get("current_location", profile.current_location)
        profile.save()

        return Response(DeliveryProfileSerializer(profile).data)


# ----------------------------
# AVAILABLE ORDERS
# ----------------------------
class AvailableOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ensure user is delivery partner
        if not hasattr(self.request.user, "delivery_profile"):
            return Order.objects.none()

        profile = self.request.user.delivery_profile

        if not profile.is_available:
            return Order.objects.none()

        return Order.objects.filter(
            status="READY",  # kitchen finished
            delivery_partner__isnull=True
        ).order_by("-created_at")


# ----------------------------
# ACCEPT ORDER
# ----------------------------
class AcceptOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id):

        # Ensure delivery partner
        if not hasattr(request.user, "delivery_profile"):
            return Response({"error": "Not a delivery partner"}, status=403)

        profile = request.user.delivery_profile

        if not profile.is_available:
            return Response({"error": "You are offline"}, status=400)

        with transaction.atomic():
            order = (
                Order.objects
                .select_for_update()
                .filter(id=order_id, delivery_partner__isnull=True, status="READY")
                .first()
            )

            if not order:
                return Response({"error": "Order already taken"}, status=400)

            order.delivery_partner = request.user
            order.status = "PICKED_UP"
            order.save()

        return Response(OrderSerializer(order).data)
# ----------------------------
# UPDATE DELIVERY STATUS
# ----------------------------
class UpdateDeliveryStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id):

        # must be delivery partner
        if not hasattr(request.user, "delivery_profile"):
            return Response({"error": "Not delivery partner"}, status=403)

        order = get_object_or_404(
            Order,
            id=order_id,
            delivery_partner=request.user
        )

        new_status = request.data.get("status")

        if new_status not in ["OUT_FOR_DELIVERY", "DELIVERED"]:
            return Response({"error": "Invalid status"}, status=400)

        order.status = new_status
        order.save()

        return Response(OrderSerializer(order).data)
# ----------------------------
# MY ACTIVE DELIVERIES
# ----------------------------
class MyDeliveriesView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if not hasattr(self.request.user, "delivery_profile"):
            return Order.objects.none()

        return Order.objects.filter(
            delivery_partner=self.request.user
        ).exclude(status="DELIVERED").order_by("-created_at")
