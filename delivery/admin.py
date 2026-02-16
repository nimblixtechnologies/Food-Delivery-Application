from django.contrib import admin
from .models import DeliveryProfile

@admin.register(DeliveryProfile)
class DeliveryProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_available', 'current_location', 'joined_at')
    list_filter = ('is_available', 'joined_at')
    search_fields = ('user__username', 'current_location')
