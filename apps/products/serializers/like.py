from rest_framework.serializers import ModelSerializer

from apps.products.models import Like


class LikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "user", "product", "created_at"]
        read_only_fields = ["id", "created_at"]
