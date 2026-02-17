from django.urls import path
from .views import DeliveryStatusView, AvailableOrdersView, AcceptOrderView
from .views import UpdateDeliveryStatusView
from .views import MyDeliveriesView



urlpatterns = [
    path('status/', DeliveryStatusView.as_view(), name='delivery-status'),
    path('orders/available/', AvailableOrdersView.as_view(), name='available-orders'),
    path('orders/<int:order_id>/accept/', AcceptOrderView.as_view(), name='accept-order'),
    path('orders/<int:order_id>/update/', UpdateDeliveryStatusView.as_view()),
    path('orders/my/', MyDeliveriesView.as_view()),

]
