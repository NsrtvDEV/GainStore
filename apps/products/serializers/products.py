from rest_framework.serializers import ModelSerializer

from apps.products.models import Product


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "name",
            "slug",
            "price",
            "cost_price",
            "discount_price",
            "discount_until",
            "stock",
            "brand",
            "weight_grams",
            "flavor",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
