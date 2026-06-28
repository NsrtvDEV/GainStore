from rest_framework import serializers

from apps.orders.models import Order, OrderItem
from apps.users.models import Address


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_slug = serializers.CharField(source="product.slug", read_only=True)
    profit = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "product_slug",
            "quantity",
            "price_snapshot",
            "cost_price_snapshot",
            "profit",
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    address = serializers.SerializerMethodField()

    def get_address(self, obj):
        return {
            "id": obj.address.id,
            "name": obj.address.name,
            "latitude": obj.address.latitude,
            "longitude": obj.address.longitude,
        }

    class Meta:
        model = Order
        fields = ["id", "status", "total_price", "address", "items", "created_at"]


class CreateOrderSerializer(serializers.Serializer):
    address_id = serializers.IntegerField()

    def validate_address_id(self, value):
        user = self.context["request"].user
        if not Address.objects.filter(id=value, user=user).exists():
            raise serializers.ValidationError("Address not found")
        return value
