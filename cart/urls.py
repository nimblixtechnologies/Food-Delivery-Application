from django.urls import path
from .views import CalculateTotalAPIView

urlpatterns = [
    path("calculate/", CalculateTotalAPIView.as_view(), name="calculate-total"),
]
