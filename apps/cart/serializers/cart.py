from rest_framework import serializers
from apps.cart.models import Cart, CartItem
from apps.products.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_slug = serializers.CharField(source="product.slug", read_only=True)
    product_price = serializers.DecimalField(
        source="product.current_price", max_digits=12, decimal_places=2, read_only=True
    )
    total = serializers.SerializerMethodField()

    def get_total(self, obj):
        return obj.product.current_price * obj.quantity

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "product_name",
            "product_slug",
            "product_price",
            "quantity",
            "total",
        ]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    def get_total(self, obj):
        return obj.get_total()

    class Meta:
        model = Cart
        fields = ["id", "items", "total"]


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("Product not found or inactive")
        return value


class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
