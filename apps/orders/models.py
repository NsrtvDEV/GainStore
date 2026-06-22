from django.db import models
from django.conf import settings


class OrderStatus(models.TextChoices):
    CREATED = "created", "Created"
    ACCEPTED = "accepted", "Accepted"
    SHIPPING = "shipping", "Shipping"
    DELIVERED = "delivered", "Delivered"
    CANCELLED = "cancelled", "Cancelled"


class PaymentMethod(models.TextChoices):
    PAYME = "payme", "Payme"
    CLICK = "click", "Click"
    CASH = "cash", "Cash"


class PaymentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PAID = "paid", "Paid"
    FAILED = "failed", "Failed"
    REFUNDED = "refunded", "Refunded"


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders"
    )
    address = models.ForeignKey(
        "users.Address", on_delete=models.PROTECT, related_name="orders"
    )
    status = models.CharField(
        max_length=20, choices=OrderStatus.choices, default=OrderStatus.CREATED
    )
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "orders"

    def __str__(self):
        return f"Order #{self.id} — {self.user.phone} ({self.status})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        "products.Product", on_delete=models.PROTECT, related_name="order_items"
    )
    quantity = models.PositiveIntegerField()
    # фиксируем цены на момент заказа — не теряем историю при изменении цен
    price_snapshot = models.DecimalField(max_digits=12, decimal_places=2)
    cost_price_snapshot = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = "order_items"

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

    @property
    def profit(self):
        return (self.price_snapshot - self.cost_price_snapshot) * self.quantity


class OrderStatusTransition(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="status_transitions"
    )
    from_status = models.CharField(max_length=20)
    to_status = models.CharField(max_length=20)
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "order_status_transitions"

    def __str__(self):
        return f"Order #{self.order_id}: {self.from_status} → {self.to_status}"


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="payments")
    method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    status = models.CharField(
        max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    external_id = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "payments"

    def __str__(self):
        return f"Payment #{self.id} — {self.method} ({self.status})"


class DeliveryTracking(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tracking")
    status = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "delivery_tracking"

    def __str__(self):
        return f"Tracking Order #{self.order_id} — {self.status}"
