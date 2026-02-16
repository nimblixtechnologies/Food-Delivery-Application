from django.urls import path
from .views import (
    RestaurantCreateView, RestaurantDetailView, RestaurantListView,
    MenuDetailView, MenuItemCreateView, MenuItemUpdateDeleteView
)

urlpatterns = [
    path('register/', RestaurantCreateView.as_view(), name='restaurant-register'),
    path('manage/', RestaurantDetailView.as_view(), name='restaurant-manage'),
    path('list/', RestaurantListView.as_view(), name='restaurant-list'),
    path('<int:restaurant_id>/menu/', MenuDetailView.as_view(), name='restaurant-menu'),
    path('menu/items/add/', MenuItemCreateView.as_view(), name='menu-item-add'),
    path('menu/items/<int:id>/', MenuItemUpdateDeleteView.as_view(), name='menu-item-manage'),
]
