from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from apps.products.models import Review, Product
from apps.products.serializers import ReviewSerializer


class ReviewListCreateAPIView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(product__slug=self.kwargs["slug"]).order_by(
            "-created_at"
        )

    def perform_create(self, serializer):
        product = Product.objects.get(slug=self.kwargs["slug"])
        serializer.save(user=self.request.user, product=product)


class ReviewDestroyAPIView(DestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
