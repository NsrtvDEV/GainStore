from django.contrib import admin

from .models import Notification, Banner


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "to_all", "is_read", "created_at")
    list_filter = ("to_all", "is_read")
    search_fields = ("title", "user__phone")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "sort_order")
    list_filter = ("is_active",)
    search_fields = ("title",)
    ordering = ("sort_order",)
