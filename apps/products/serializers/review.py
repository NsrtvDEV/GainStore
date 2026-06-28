from rest_framework.serializers import ModelSerializer

from apps.products.models import Review


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "id",
            "product",
            "user",
            "rating",
            "comment",
            "created_at",
            "updated_at",
        ]
        read_only_fileds = ["id", "created_at", "updated_at"]
