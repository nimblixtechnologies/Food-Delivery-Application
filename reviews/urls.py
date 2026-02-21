from django.urls import path

from .views import (
    CreatePartnerReviewView,
    CreateRestaurantReviewView,
    RestaurantReviewsView,
    ReviewListView,
)

urlpatterns = [
    path('', ReviewListView.as_view(), name='review-list'),
    path('orders/<int:order_id>/restaurant/', CreateRestaurantReviewView.as_view(), name='create-restaurant-review'),
    path('orders/<int:order_id>/partner/', CreatePartnerReviewView.as_view(), name='create-partner-review'),
    path('restaurants/<int:restaurant_id>/', RestaurantReviewsView.as_view(), name='restaurant-reviews'),
]
