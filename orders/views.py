from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem, Order, OrderItem
from .serializers import (
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    PlaceOrderSerializer,
    DeliveryPartnerStatusUpdateSerializer
)
from restaurants.models import MenuItem
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

class CartView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        menu_item_id = request.data.get('menu_item_id')
        quantity = int(request.data.get('quantity', 1))

        menu_item = get_object_or_404(MenuItem, id=menu_item_id)
        
        # Check if cart has items from another restaurant
        if cart.items.exists():
            existing_restaurant = cart.items.first().menu_item.menu.restaurant
            if existing_restaurant != menu_item.menu.restaurant:
                return Response({'error': 'Cannot add items from different restaurants'}, status=status.HTTP_400_BAD_REQUEST)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=menu_item)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        return Response(CartSerializer(cart).data)

    def delete(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        return Response({'message': 'Cart cleared'})

class CheckoutView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        if not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        restaurant = cart.items.first().menu_item.menu.restaurant
        total_amount = cart.total_price()
        
        order = Order.objects.create(
            customer=request.user,
            restaurant=restaurant,
            total_amount=total_amount,
            delivery_address=request.data.get('delivery_address', 'Default Address')
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                menu_item_name=item.menu_item.name,
                quantity=item.quantity,
                price=item.menu_item.price
            )
        
        cart.items.all().delete()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)

class OrderUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

# ======================================================
# Delivery Partner Updates Order Status API
# ======================================================

from delivery.models import DeliveryProfile

class DeliveryPartnerUpdateStatusAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, order_id):

        user = request.user

        # ✅ Only Delivery Partner role allowed
        if user.role != "DELIVERY":
            return Response(
                {"error": "Only delivery partners can update status"},
                status=status.HTTP_403_FORBIDDEN
            )

        # ✅ Order exists?
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # ✅ Must be assigned partner
        if order.delivery_partner != user:
            return Response(
                {"error": "This order is not assigned to you"},
                status=status.HTTP_403_FORBIDDEN
            )

        # ✅ Update status
        serializer = DeliveryPartnerStatusUpdateSerializer(
            order,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Order status updated successfully",
                    "order_id": order.id,
                    "new_status": order.status
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

