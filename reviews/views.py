from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order
from restaurants.models import Restaurant

from .models import Review
from .serializers import CreateReviewSerializer, ReviewSerializer


def validate_review_order_and_customer(order_id, customer):
	order = get_object_or_404(Order, id=order_id)

	if order.customer_id != customer.id:
		raise PermissionDenied('Only order customer can submit review')

	if order.status != Order.Status.DELIVERED:
		raise ValidationError('Order must be delivered before review')

	return order


class CreateRestaurantReviewView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request, order_id):
		serializer = CreateReviewSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		order = validate_review_order_and_customer(order_id, request.user)

		if Review.objects.filter(
			order=order,
			customer=request.user,
			restaurant=order.restaurant
		).exists():
			return Response(
				{'error': 'Restaurant review already exists for this order'},
				status=status.HTTP_409_CONFLICT
			)

		review = Review.objects.create(
			order=order,
			customer=request.user,
			restaurant=order.restaurant,
			rating=serializer.validated_data['rating'],
			comment=serializer.validated_data.get('comment')
		)
		return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)


class CreatePartnerReviewView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request, order_id):
		serializer = CreateReviewSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		order = validate_review_order_and_customer(order_id, request.user)

		if not order.delivery_partner_id:
			raise ValidationError('Order has no delivery partner assigned')

		if Review.objects.filter(
			order=order,
			customer=request.user,
			partner=order.delivery_partner
		).exists():
			return Response(
				{'error': 'Partner review already exists for this order'},
				status=status.HTTP_409_CONFLICT
			)

		review = Review.objects.create(
			order=order,
			customer=request.user,
			partner=order.delivery_partner,
			rating=serializer.validated_data['rating'],
			comment=serializer.validated_data.get('comment')
		)
		return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)


class ReviewListView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request):
		items = Review.objects.filter(customer=request.user)
		return Response({'items': ReviewSerializer(items, many=True).data})


class RestaurantReviewsView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request, restaurant_id):
		restaurant = get_object_or_404(Restaurant, id=restaurant_id)
		restaurant_reviews = Review.objects.filter(restaurant=restaurant)

		rating_count = restaurant_reviews.count()
		average_rating = restaurant_reviews.aggregate(avg=Avg('rating'))['avg'] or 0.0

		return Response(
			{
				'restaurant_id': restaurant.id,
				'restaurant_name': restaurant.name,
				'rating_count': rating_count,
				'average_rating': round(float(average_rating), 2),
				'reviews': ReviewSerializer(restaurant_reviews, many=True).data,
			}
		)
