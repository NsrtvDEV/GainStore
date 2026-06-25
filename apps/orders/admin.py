from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import Order, OrderItem, OrderStatusTransition, Payment, DeliveryTracking


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    fields = ("product", "quantity", "price_snapshot", "cost_price_snapshot")
    readonly_fields = ("price_snapshot", "cost_price_snapshot")


class OrderStatusTransitionInline(TabularInline):
    model = OrderStatusTransition
    extra = 0
    fields = ("from_status", "to_status", "reason", "created_at")
    readonly_fields = ("created_at",)


class PaymentInline(TabularInline):
    model = Payment
    extra = 0
    fields = ("method", "status", "amount", "external_id")


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ("id", "user", "status", "total_price", "created_at")
    list_filter = ("status",)
    search_fields = ("user__phone", "id")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    inlines = [OrderItemInline, PaymentInline, OrderStatusTransitionInline]


@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    list_display = (
        "id",
        "order",
        "product",
        "quantity",
        "price_snapshot",
        "cost_price_snapshot",
    )
    search_fields = ("order__id", "product__name")


@admin.register(OrderStatusTransition)
class OrderStatusTransitionAdmin(ModelAdmin):
    list_display = ("order", "from_status", "to_status", "reason", "created_at")
    list_filter = ("from_status", "to_status")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)


@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    list_display = (
        "id",
        "order",
        "method",
        "status",
        "amount",
        "external_id",
        "created_at",
    )
    list_filter = ("method", "status")
    search_fields = ("order__id", "external_id")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(DeliveryTracking)
class DeliveryTrackingAdmin(ModelAdmin):
    list_display = ("order", "status", "latitude", "longitude", "created_at")
    list_filter = ("status",)
    search_fields = ("order__id",)
    ordering = ("-created_at",)
