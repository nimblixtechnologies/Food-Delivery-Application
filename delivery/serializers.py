from rest_framework import serializers
from .models import DeliveryRating
from django.db.models import Avg

class DeliveryRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryRating
        fields = ['id', 'order', 'partner', 'score', 'review_text']

    def create(self, validated_data):

        rating = DeliveryRating.objects.create(**validated_data)
        partner = validated_data['partner']
        stats = DeliveryRating.objects.filter(partner=partner).aggregate(Avg('score'))
        partner.average_rating = round(stats['score__avg'] or 0, 2)
        partner.save()
        
        return rating