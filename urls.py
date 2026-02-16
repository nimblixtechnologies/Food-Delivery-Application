from django.urls import path
from .views import AdminOrderView

urlpatterns = [
    path('admin/orders/', AdminOrderView.as_view(), name='admin-orders'),
]
