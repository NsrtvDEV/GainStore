from django.db import models

from apps.users.models import User, Address
from apps.products.models import Product


class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, related_name="orders"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "orders"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, related_name="order_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # цена на момент покупки

    class Meta:
        db_table = "order_items"


class OrderStatusTransition(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="status_transitions"
    )
    from_status = models.CharField(max_length=20)
    to_status = models.CharField(max_length=20)
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "order_status_transition"


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    method = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    external_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "payments"


class DeliveryTracking(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tracking")
    status = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "delivery_tracking"
