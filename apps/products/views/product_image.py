from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser

from apps.products.models import ProductImage, Product
from apps.products.serializers import ProductImageSerializer


class ProductImageListCreateAPIView(ListCreateAPIView):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminUser]
    parsers = [MultiPartParser, FormParser]

    def get_queryset(self):
        return ProductImage.objects.filter(product__slug=self.kwargs["slug"]).order_by(
            "sort_order"
        )

    def perform_create(self, serializer):
        product = Product.objects.get(slug=self.kwargs["slug"])
        serializer.save(product=product)


class ProductImageDestroyAPIView(DestroyAPIView):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return ProductImage.objects.filter(product__slug=self.kwargs["slug"])
