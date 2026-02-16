from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils import timezone

from .models import Complaint
from .serializers import ComplaintSerializer
from flasheatsapps.orders.models import Order


class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    def update(self, request, *args, **kwargs):
        complaint = self.get_object()

        # Only admin can approve/reject
        if not request.user.is_staff:
            return Response({"error": "Only admin can update complaint status."},
                            status=status.HTTP_403_FORBIDDEN)

        status_value = request.data.get("status")

        if status_value == "Approved":
            complaint.status = "Approved"
            complaint.resolved_at = timezone.now()

            order = complaint.order
            order.refund_status = "Refunded"
            order.refund_amount = order.total_amount
            order.status = "Refunded"

            order.save()
            complaint.save()

            return Response({"message": "Complaint approved and refund processed."})

        elif status_value == "Rejected":
            complaint.status = "Rejected"
            complaint.resolved_at = timezone.now()
            complaint.save()

            return Response({"message": "Complaint rejected."})

        return Response({"error": "Invalid status value."})
