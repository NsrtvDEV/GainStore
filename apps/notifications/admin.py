from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Notification, Banner


@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    list_display = ("id", "title", "user", "to_all", "is_read", "created_at")
    list_filter = ("to_all", "is_read")
    search_fields = ("title", "user__phone")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Banner)
class BannerAdmin(ModelAdmin):
    list_display = ("id", "title", "is_active", "sort_order")
    list_filter = ("is_active",)
    search_fields = ("title",)
    ordering = ("sort_order",)
