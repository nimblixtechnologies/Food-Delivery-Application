from rest_framework import serializers
from .models import Complaint
from django.utils import timezone

class ComplaintSerializer(serializers.ModelSerializer):

    class Meta:
        model = Complaint
        fields = '__all__'
        read_only_fields = ['customer', 'resolved_at']

    def validate(self, data):
        order = data['order']
        if order.status != 'Delivered':
            raise serializers.ValidationError("Complaint can only be raised for delivered orders.")
        return data
