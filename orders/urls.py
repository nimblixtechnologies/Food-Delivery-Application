from django.urls import path
from .views import CartView, CheckoutView, OrderListView, OrderUpdateView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('my-orders/', OrderListView.as_view(), name='my-orders'),
    path('<int:id>/update-status/', OrderUpdateView.as_view(), name='update-order-status'),
]
