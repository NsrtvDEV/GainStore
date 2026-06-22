from django.db import models
from django.conf import settings


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True,  # null если to_all=True (всем пользователям)
    )
    to_all = models.BooleanField(default=False)
    title = models.CharField(max_length=150)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "notifications"

    def __str__(self):
        if self.to_all:
            return f"[ALL] {self.title}"
        return f"{self.user} — {self.title}"


class Banner(models.Model):
    title = models.CharField(max_length=150, blank=True, null=True)
    image_url = models.CharField(max_length=255)
    link_url = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "banners"
        ordering = ["sort_order"]

    def __str__(self):
        return self.title or f"Banner #{self.id}"
