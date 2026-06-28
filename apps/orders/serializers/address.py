from rest_framework import serializers
from apps.users.models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id", "name", "latitude", "longitude", "created_at"]
        read_only_fields = ["id", "created_at"]
