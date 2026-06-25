from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    SendOtpAPIView,
    VerifyOtpAPIView,
    LogoutAPIView,
    MeAPIView,
    BalanceAPIView,
    UserProfileUpdateAPIView,
)

urlpatterns = [
    path("send-otp/", SendOtpAPIView.as_view(), name="send-otp"),
    path("verify-otp/", VerifyOtpAPIView.as_view(), name="verify-otp"),
    path("refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("me/", MeAPIView.as_view(), name="me"),
    path("balance/", BalanceAPIView.as_view(), name="balance"),
    path("me/update/", UserProfileUpdateAPIView.as_view(), name="me-update"),
]
