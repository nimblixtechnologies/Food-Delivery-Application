from rest_framework import serializers
from .models import Restaurant, Menu, MenuItem, Category

# -------------------------------
# MenuItem Serializers
# -------------------------------
class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = [
            'id', 'name', 'description', 'price', 
            'is_veg', 'is_available', 'image'
        ]

class CreateMenuItemSerializer(serializers.ModelSerializer):
    """
    Serializer used for creating/updating Menu Items
    """
    class Meta:
        model = MenuItem
        fields = [
            'name', 'description', 'price', 
            'is_veg', 'is_available', 'image'
        ]

# -------------------------------
# Menu Serializers
# -------------------------------
class MenuSerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = ['id', 'items']

# -------------------------------
# Restaurant Serializers
# -------------------------------
class RestaurantSerializer(serializers.ModelSerializer):
    menu = MenuSerializer(read_only=True)
    
    class Meta:
        model = Restaurant
        fields = [
            'id', 'name', 'address', 'contact_number', 
            'is_approved', 'menu'
        ]
        read_only_fields = ['is_approved']

class CreateRestaurantSerializer(serializers.ModelSerializer):
    """
    Serializer used for restaurant creation
    """
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'contact_number']

# -------------------------------
# Category Serializer
# -------------------------------
class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Restaurant Categories
    """
    class Meta:
        model = Category
        fields = '__all__'
