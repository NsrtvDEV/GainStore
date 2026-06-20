from django.db import models

from apps.users.models import User


class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True,
    )
    to_all = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notifications"
