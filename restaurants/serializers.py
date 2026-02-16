from rest_framework import serializers
from .models import Restaurant, Menu, MenuItem
from django.contrib.auth import get_user_model

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'is_veg', 'is_available', 'image']

class MenuSerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = ['id', 'items']

class RestaurantSerializer(serializers.ModelSerializer):
    menu = MenuSerializer(read_only=True)
    
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'contact_number', 'is_approved', 'menu']
        read_only_fields = ['is_approved']

class CreateRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'contact_number']

class CreateMenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'is_veg', 'is_available', 'image']

User = get_user_model()

class RestaurantRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'contact_number', 'email', 'password']

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            role='RESTAURANT'
        )

        restaurant = Restaurant.objects.create(
            user=user,
            **validated_data
        )

        Menu.objects.create(restaurant=restaurant)

        return restaurant
