from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser

from apps.products.models import Product
from apps.products.serializers import ProductSerializer


class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all().order_by("name")
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return [IsAdminUser()]


class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all().order_by("name")
    serializer_class = ProductSerializer
    lookup_field = "slug"

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return [IsAdminUser()]
