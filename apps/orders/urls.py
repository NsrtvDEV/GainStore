from django.urls import path
from .views import OrderListAPIView, OrderRetrieveAPIView, CreateOrderAPIView

urlpatterns = [
    path("", CreateOrderAPIView.as_view(), name="order-create"),  # POST
    path("", OrderListAPIView.as_view(), name="order-list"),  # GET
    path("<int:pk>/", OrderRetrieveAPIView.as_view(), name="order-detail"),
]
