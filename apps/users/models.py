from django.db import models


class User(models.Model):
    ROLE_CHOICES = (
        ("customer", "Customer"),
        ("admin", "Admin"),
        ("courier", "Courier"),
    )

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="customer")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        db_table = "addresses"

    def __str__(self):
        return self.name


class TokenBlackList(models.Model):
    token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "token_black_list"


class OtpCode(models.Model):
    phone = models.CharField(max_length=20)
    code = models.CharField(max_length=10)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "otp_codes"
