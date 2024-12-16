from django.db import models
from users.models import BaseUser
from products.models import Product


class CartModel(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='carts')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_expired = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def mark_as_expired(self):
        self.is_expired = True
        self.save()

    def __str__(self):
        return {self.id}


class CartItems(models.Model):
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)