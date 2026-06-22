from django.contrib import admin

from .models import Category, Product, ProductImage, Review, Like


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "parent")
    search_fields = ("name", "slug")
    ordering = ("name",)


class ProductImageInline(admin.TabularInline):
    """Позволяет добавлять фото товара прямо на странице товара"""

    model = ProductImage
    extra = 1
    fields = ("url", "is_main", "sort_order")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "cost_price",
        "discount_price",
        "stock",
        "is_active",
    )
    list_filter = ("category", "is_active", "brand")
    search_fields = ("name", "brand", "slug")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    inlines = [ProductImageInline]

    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                    "category",
                    "name",
                    "slug",
                    "brand",
                    "flavor",
                    "weight_grams",
                    "description",
                )
            },
        ),
        (
            "Цены",
            {"fields": ("price", "cost_price", "discount_price", "discount_until")},
        ),
        ("Склад", {"fields": ("stock", "is_active")}),
        ("Даты", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "url", "is_main", "sort_order")
    list_filter = ("is_main",)
    search_fields = ("product__name",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("product__name", "user__phone")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "created_at")
    search_fields = ("user__phone", "product__name")
    ordering = ("-created_at",)
