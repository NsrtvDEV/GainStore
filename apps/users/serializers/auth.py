from django.core.validators import RegexValidator
from rest_framework import serializers

from apps.users.models import User


class SendOtpSerializer(serializers.Serializer):
    phone = serializers.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^\+998\d{9}$", message="Phone must be in format +998XXXXXXXXX"
            )
        ],
    )


class VerifyOtpSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    code = serializers.CharField(max_length=6)
    first_name = serializers.CharField(max_length=50, required=False, default="User")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "phone", "first_name", "last_name", "role", "is_active")


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]
