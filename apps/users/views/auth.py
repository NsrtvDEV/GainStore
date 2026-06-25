from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema


from apps.users.models import User, OtpCode
from apps.users.serializers import (
    SendOtpSerializer,
    VerifyOtpSerializer,
    UserSerializer,
    UserUpdateSerializer,
)
from apps.users.utils import send_sms, generate_code, get_balance


OTP_LIFETIME_SECONDS = 120


class SendOtpAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=SendOtpSerializer)  # ← добавь
    def post(self, request):
        serializer = SendOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data["phone"]
        code = generate_code()

        OtpCode.objects.create(
            phone=phone,
            code=code,
            is_used=False,
            expires_at=timezone.now() + timedelta(seconds=OTP_LIFETIME_SECONDS),
        )

        send_sms(phone, f"UICdev platformasiga kirish uchun kod: {code}")

        return Response(
            {"message": "OTP code sent", "expires_in": OTP_LIFETIME_SECONDS},
            status=status.HTTP_200_OK,
        )


class VerifyOtpAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=VerifyOtpSerializer)  # ← добавь
    def post(self, request):
        serializer = VerifyOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data["phone"]
        code = serializer.validated_data["code"]
        first_name = serializer.validated_data["first_name"]

        # берём последний неиспользованный код для этого номера
        otp = (
            OtpCode.objects.filter(phone=phone, is_used=False)
            .order_by("-created_at")
            .first()
        )

        if not otp or otp.code != code:
            return Response(
                {"error": "Invalid code"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if otp.expires_at < timezone.now():
            return Response(
                {"error": "Code expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # помечаем код использованным
        otp.is_used = True
        otp.save(update_fields=["is_used"])

        # создаём пользователя если новый, иначе берём существующего
        user, is_new_user = User.objects.get_or_create(
            phone=phone,
            defaults={"first_name": first_name, "is_active": True},
        )

        # выдаём JWT токены
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "is_new_user": is_new_user,
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class LogoutAPIView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out"}, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class BalanceAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        balance = get_balance()
        return Response(balance)


class UserProfileUpdateAPIView(UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)
