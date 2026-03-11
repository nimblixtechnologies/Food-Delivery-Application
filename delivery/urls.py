from django.urls import path
from .views import DeliveryStatusView, AvailableOrdersView, AcceptOrderView, RatePartnerView

urlpatterns = [
    path('status/', DeliveryStatusView.as_view(), name='delivery-status'),
    path('orders/available/', AvailableOrdersView.as_view(), name='available-orders'),
    path('orders/<int:order_id>/accept/', AcceptOrderView.as_view(), name='accept-order'),
    path('rate/', RatePartnerView.as_view(), name='rate-delivery-partner'),
]