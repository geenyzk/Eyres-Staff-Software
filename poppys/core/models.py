# core/models.py

from django.db import models
from accounts.models import CustomUser

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def total(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.item_name} ({self.user.username})"


class Sale(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    sold_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    sold_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale: {self.order.item_name} by {self.sold_by.username if self.sold_by else 'Unknown'}"