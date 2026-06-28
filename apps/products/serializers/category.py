from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    PrimaryKeyRelatedField,
    DictField,
)
from drf_spectacular.utils import extend_schema_field

from apps.products.models import Category


class CategorySerializer(ModelSerializer):
    """Для создания/обновления — parent как ID"""

    parent = PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "icon_url", "parent"]


class CategoryDetailSerializer(ModelSerializer):
    """Для чтения — parent как объект"""

    parent = SerializerMethodField()

    @extend_schema_field(DictField())
    def get_parent(self, obj):
        if obj.parent:
            return {"id": obj.parent.id, "name": obj.parent.name}
        return None

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "icon_url", "parent"]
