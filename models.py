from django.db import models

# Create your models here.

class Order(models.Model):
    STATUS_CHOICES = [
        ('ONGOING','Ongoing'),
        ('COMPLETED','Completed'),
    ]


    customer_name = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.status}"
    