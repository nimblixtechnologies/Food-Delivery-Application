from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, MenuItemViewSet, RestaurantViewSet,
    RestaurantCreateView, RestaurantDetailView, RestaurantListView,
    MenuDetailView, MenuItemCreateView, MenuItemUpdateDeleteView
)

# create a router instance
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'menu-items', MenuItemViewSet)
router.register(r'restaurants', RestaurantViewSet)

urlpatterns = [
    # router API endpoints
    path('api/', include(router.urls)),

    # Class-based views
    path('register/', RestaurantCreateView.as_view(), name='restaurant-register'),
    path('manage/', RestaurantDetailView.as_view(), name='restaurant-manage'),
    path('list/', RestaurantListView.as_view(), name='restaurant-list'),
    path('<int:restaurant_id>/menu/', MenuDetailView.as_view(), name='restaurant-menu'),
    path('menu/items/add/', MenuItemCreateView.as_view(), name='menu-item-add'),
    path('menu/items/<int:id>/', MenuItemUpdateDeleteView.as_view(), name='menu-item-manage'),
]
