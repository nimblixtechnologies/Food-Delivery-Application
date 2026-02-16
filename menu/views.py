from rest_framework.viewsets import ModelViewSet
from .models import MenuItem
from .serializers import MenuItemSerializer

class MenuItemViewSet(ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
