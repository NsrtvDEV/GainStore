from rest_framework.generics import ListCreateAPIView, DestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from apps.products.models import Like
from apps.products.serializers import LikeSerializer


class LikeListCreateAPIView(ListCreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeDestroyAPIView(DestroyAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user)

    def get_object(self):
        product_id = self.kwargs.get("product_id")
        return get_object_or_404(Like, user=self.request.user, product_id=product_id)
