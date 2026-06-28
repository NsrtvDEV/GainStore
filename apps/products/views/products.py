from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)
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
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_object(self):
        lookup = self.kwargs["lookup"]
        if lookup.isdigit():
            obj = get_object_or_404(Product, pk=lookup)
        else:
            obj = get_object_or_404(Product, slug=lookup)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return [IsAdminUser()]
