from django.urls import path
from .views import (
    ProductListCreateAPIView,
    ProductRetrieveUpdateDestroyAPIView,
    CategoryListCreateAPIView,
    CategoryRetrieveUpdateDestroyAPIView,
    LikeListCreateAPIView,
    LikeDestroyAPIView,
    ReviewDestroyAPIView,
    ReviewListCreateAPIView,
    ProductImageListCreateAPIView,
    ProductImageDestroyAPIView,
)

urlpatterns = [
    path("categories/", CategoryListCreateAPIView.as_view(), name="category-list"),
    path(
        "categories/<int:pk>/",
        CategoryRetrieveUpdateDestroyAPIView.as_view(),
        name="category-detail",
    ),
    path("products/", ProductListCreateAPIView.as_view(), name="product-list"),
    path(
        "products/<str:lookup>/",
        ProductRetrieveUpdateDestroyAPIView.as_view(),
        name="product-detail",
    ),
    path("likes/<int:product_id>/", LikeDestroyAPIView.as_view(), name="like-destroy"),
    path("likes/", LikeListCreateAPIView.as_view(), name="like-list"),
    path(
        "products/<slug:slug>/reviews/",
        ReviewListCreateAPIView.as_view(),
        name="review-list",
    ),
    path("reviews/<int:pk>/", ReviewDestroyAPIView.as_view(), name="review-delete"),
    path(
        "products/<slug:slug>/images/",
        ProductImageListCreateAPIView.as_view(),
        name="product-images",
    ),
    path(
        "products/<slug:slug>/images/<int:pk>/",
        ProductImageDestroyAPIView.as_view(),
        name="product-image-delete",
    ),
]
