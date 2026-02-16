from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import Order
from .serializers import OrderSerializer

# Create your views here.

class AdminOrderView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        status = request.query_params.get('status')

        if status:
            orders = Order.objects.filter(status=status.upper())
        else:
            orders = Order.objects.all()

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)