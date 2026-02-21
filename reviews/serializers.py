from rest_framework import serializers

from .models import Review


class CreateReviewSerializer(serializers.Serializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)
    comment = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=500)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id',
            'order',
            'customer',
            'restaurant',
            'partner',
            'rating',
            'comment',
            'created_at',
        ]
        read_only_fields = fields
