from django.urls import path

from .views.account import UserAccountView
from .views.auth import (
    ChangePasswordView,
    ForgotPasswordView,
    LoginView,
    RegisterView,
    ResendVerificationView,
    ResetPasswordView,
    VerifyAccountView,
)

urlpatterns = [
    path("auth/register", RegisterView.as_view(), name="register-view"),
    path("auth/verify", VerifyAccountView.as_view(), name="verify-account-view"),
    path("auth/resend-otp", ResendVerificationView.as_view(), name="resend-otp-view"),
    path("auth/login", LoginView.as_view(), name="login-view"),
    path(
        "auth/forgot-password",
        ForgotPasswordView.as_view(),
        name="forgot-password-view",
    ),
    path(
        "auth/reset-password", ResetPasswordView.as_view(), name="reset-password-view"
    ),
    path(
        "auth/change-password",
        ChangePasswordView.as_view(),
        name="change-password-view",
    ),
    path(
        "account",
        UserAccountView.as_view(),
        name="account-view",
    ),
]
