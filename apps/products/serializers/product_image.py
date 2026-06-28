from rest_framework.serializers import ModelSerializer

from apps.products.models import ProductImage


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "url", "is_main", "sort_order"]
