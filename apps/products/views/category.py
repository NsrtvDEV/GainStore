from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser

from apps.products.models import Category
from apps.products.serializers import CategorySerializer, CategoryDetailSerializer


class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all().order_by("name")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CategorySerializer  # для создания
        return CategoryDetailSerializer  # для чтения

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return [IsAdminUser()]


class CategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return [IsAdminUser()]
