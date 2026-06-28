from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from apps.cart.models import Cart, CartItem
from apps.cart.serializers import (
    CartSerializer,
    AddToCartSerializer,
    UpdateCartItemSerializer,
)
from apps.products.models import Product


def get_or_create_cart(user):
    """Получить или создать корзину пользователя"""
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


class CartAPIView(APIView):
    """GET /cart/ — получить корзину с товарами и общей суммой"""

    permission_classes = [IsAuthenticated]

    @extend_schema(responses=CartSerializer)
    def get(self, request):
        cart = get_or_create_cart(request.user)
        return Response(CartSerializer(cart).data)


class AddToCartAPIView(APIView):
    """POST /cart/add/ — добавить товар в корзину"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data["product_id"]
        quantity = serializer.validated_data["quantity"]
        product = Product.objects.get(id=product_id)
        cart = get_or_create_cart(request.user)

        # если товар уже в корзине — увеличиваем quantity
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity},
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save(update_fields=["quantity"])

        return Response(
            CartSerializer(cart).data,
            status=status.HTTP_200_OK,
        )


class CartItemUpdateDestroyAPIView(APIView):
    """
    PATCH /cart/items/{id}/ — изменить количество товара
    DELETE /cart/items/{id}/ — удалить товар из корзины
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        try:
            return CartItem.objects.get(pk=pk, cart__user=request.user)
        except CartItem.DoesNotExist:
            return None

    def patch(self, request, pk):
        cart_item = self.get_object(request, pk)
        if not cart_item:
            return Response(
                {"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart_item.quantity = serializer.validated_data["quantity"]
        cart_item.save(update_fields=["quantity"])

        return Response(CartSerializer(cart_item.cart).data)

    def delete(self, request, pk):
        cart_item = self.get_object(request, pk)
        if not cart_item:
            return Response(
                {"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND
            )

        cart = cart_item.cart
        cart_item.delete()

        return Response(CartSerializer(cart).data)


class ClearCartAPIView(APIView):
    """DELETE /cart/clear/ — очистить всю корзину"""

    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cart = get_or_create_cart(request.user)
        cart.items.all().delete()
        return Response({"message": "Cart cleared"}, status=status.HTTP_200_OK)
