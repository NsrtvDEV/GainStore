from django.db import models

from apps.users.models import User
from apps.products.models import Product


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="carts"
    )
    session_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "carts"


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = "cart_items"
        unique_together = ("user", "product")
