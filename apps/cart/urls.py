from django.urls import path
from .views import (
    CartAPIView,
    AddToCartAPIView,
    CartItemUpdateDestroyAPIView,
    ClearCartAPIView,
)

urlpatterns = [
    path("", CartAPIView.as_view(), name="cart"),
    path("add/", AddToCartAPIView.as_view(), name="cart-add"),
    path("items/<int:pk>/", CartItemUpdateDestroyAPIView.as_view(), name="cart-item"),
    path("clear/", ClearCartAPIView.as_view(), name="cart-clear"),
]
