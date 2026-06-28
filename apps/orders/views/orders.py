from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cart.models import Cart
from apps.orders.models import Order, OrderItem, OrderStatusTransition
from apps.orders.serializers import OrderSerializer, CreateOrderSerializer
from apps.users.models import Address


class OrderListAPIView(ListAPIView):
    """GET /orders/ — список моих заказов"""

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Order.objects.filter(user=self.request.user)
            .prefetch_related("items__product")
            .order_by("-created_at")
        )


class OrderRetrieveAPIView(RetrieveAPIView):
    """GET /orders/{id}/ — детали заказа"""

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class CreateOrderAPIView(APIView):
    """POST /orders/ — оформить заказ из корзины"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateOrderSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        address_id = serializer.validated_data["address_id"]

        # получаем корзину пользователя
        try:
            cart = Cart.objects.prefetch_related("items__product").get(
                user=request.user
            )
        except Cart.DoesNotExist:
            return Response(
                {"error": "Cart not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not cart.items.exists():
            return Response(
                {"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST
            )

        address = Address.objects.get(id=address_id)
        total_price = cart.get_total()

        # создаём заказ
        order = Order.objects.create(
            user=request.user,
            address=address,
            total_price=total_price,
            status="created",
        )

        # переносим товары из корзины в заказ с фиксацией цен
        for item in cart.items.all():
            product = item.product
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.quantity,
                price_snapshot=product.current_price,  # фиксируем цену продажи
                cost_price_snapshot=product.cost_price,  # фиксируем себестоимость
            )

        # логируем создание заказа
        OrderStatusTransition.objects.create(
            order=order,
            from_status="",
            to_status="created",
            reason="Order created from cart",
        )

        # очищаем корзину после оформления заказа
        cart.items.all().delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

