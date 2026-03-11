from rest_framework import serializers

class CartItemSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    quantity = serializers.IntegerField()


class CalculateTotalSerializer(serializers.Serializer):
    cart_items = CartItemSerializer(many=True)
    promo_code = serializers.CharField(required=False, allow_blank=True)
