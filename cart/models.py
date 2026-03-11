from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    delivery_charge = models.FloatField(default=40)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    tax_percentage = models.FloatField(default=5)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class PromoCode(models.Model):
    code = models.CharField(max_length=20)
    discount_percentage = models.FloatField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
