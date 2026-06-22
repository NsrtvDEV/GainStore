from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import Cart, CartItem


class CartItemInline(TabularInline):
    """Показывает товары прямо внутри корзины"""

    model = CartItem
    extra = 0
    fields = ("product", "quantity", "created_at")
    readonly_fields = ("created_at",)


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ("id", "user", "session_id", "created_at")
    search_fields = ("user__phone", "session_id")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(ModelAdmin):
    list_display = ("cart", "product", "quantity", "created_at")
    search_fields = ("cart__user__phone", "product__name")
    ordering = ("-created_at",)
