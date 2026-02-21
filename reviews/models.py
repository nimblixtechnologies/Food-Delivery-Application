from django.conf import settings
from django.db import models
from django.db.models import Q

from orders.models import Order
from restaurants.models import Restaurant


class Review(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='reviews')
	customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_given')
	restaurant = models.ForeignKey(
		Restaurant,
		on_delete=models.CASCADE,
		null=True,
		blank=True,
		related_name='reviews_received'
	)
	partner = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		null=True,
		blank=True,
		related_name='partner_reviews_received'
	)
	rating = models.PositiveSmallIntegerField()
	comment = models.TextField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']
		constraints = [
			models.CheckConstraint(
				condition=Q(rating__gte=1) & Q(rating__lte=5),
				name='reviews_rating_between_1_and_5'
			),
			models.CheckConstraint(
				condition=(Q(restaurant__isnull=False) & Q(partner__isnull=True))
				| (Q(restaurant__isnull=True) & Q(partner__isnull=False)),
				name='reviews_exactly_one_target'
			),
			models.UniqueConstraint(
				fields=['order', 'customer', 'restaurant'],
				condition=Q(restaurant__isnull=False),
				name='unique_restaurant_review_per_order_customer'
			),
			models.UniqueConstraint(
				fields=['order', 'customer', 'partner'],
				condition=Q(partner__isnull=False),
				name='unique_partner_review_per_order_customer'
			),
		]

	def __str__(self):
		target = self.restaurant.name if self.restaurant else self.partner.username
		return f'Review #{self.id} - {target}'
