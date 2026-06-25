from django.contrib import admin
from unfold.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, OtpCode, Address


class UserAdmin(ModelAdmin, BaseUserAdmin):
    list_display = (
        "id",
        "phone",
        "first_name",
        "last_name",
        "role",
        "is_active",
        "is_staff",
        "created_at",
    )
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("phone", "first_name", "last_name")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Dates", {"fields": ("created_at", "updated_at", "last_login")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone", "first_name", "password1", "password2"),
            },
        ),
    )


@admin.register(OtpCode)
class OtpCodeAdmin(ModelAdmin):  # ← ModelAdmin из unfold
    list_display = ("phone", "code", "is_used", "expires_at", "created_at")
    list_filter = ("is_used",)
    search_fields = ("phone",)
    ordering = ("-created_at",)


@admin.register(Address)
class AddressAdmin(ModelAdmin):  # ← ModelAdmin из unfold
    list_display = ("name", "user", "latitude", "longitude", "created_at")
    search_fields = ("name", "user__phone")
    ordering = ("-created_at",)


admin.site.register(User, UserAdmin)
