from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken

import apps.users.tasks as task
from apps.users.serializers.auth import (
    ChangePasswordSerializer,
    EmailSerializer,
    LoginSerializer,
    RegisterSerializer,
    ResetPasswordSerializer,
    VerifyAccountSerializer,
)
from services import Cache
from utils.response import Response
from utils.utils import generate_otp, minutes_to_seconds


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    model = get_user_model()
    cache = Cache()

    def post(self, request):
        """
        Register user, send verification OTP to email and return user id
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(errors=serializer.errors, status_code=400)

        data = serializer.validated_data
        email = data.get("email")
        otp = generate_otp()
        user = self.model.objects.create_user(**data)

        task.send_verification_otp.delay([email], otp)

        cache_exp = minutes_to_seconds(5)
        self.cache.set(f"register_{user.id}", otp, cache_exp)

        return Response(
            success=True,
            message="Verify your account",
            data={"user_id": user.id},
            status_code=201,
        )


class VerifyAccountView(generics.GenericAPIView):
    serializer_class = VerifyAccountSerializer
    model = get_user_model()
    cache = Cache()

    def patch(self, request):
        """
        Verify user account by validating OTP
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(errors=serializer.errors, status_code=400)

        data = serializer.validated_data
        cached_otp = self.cache.get(f"register_{data['user_id']}")
        if not cached_otp:
            return Response(success=False, message="OTP expired", status_code=400)
        if cached_otp != data["otp"]:
            return Response(success=False, message="Invalid OTP", status_code=400)

        self.model.objects.filter(id=data["user_id"]).update(is_active=True)
        self.cache.delete(f"register_{data['user_id']}")

        return Response(success=True, message="Account verified", status_code=200)


class ResendVerificationView(generics.GenericAPIView):
    serializer_class = EmailSerializer
    model = get_user_model()
    cache = Cache()

    def post(self, request):
        """
        Resend verification OTP to email and return user id
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(errors=serializer.errors, status_code=400)

        email = serializer.validated_data["email"]
        user = self.model.objects.filter(email=email).first()
        if not user:
            return Response(
                success=True,
                message="If the email is registered, you will receive an email with the OTP",
                status_code=200,
            )
        if user.is_active:
            return Response(
                success=True, message="Account already verified", status_code=200
            )

        otp = generate_otp()
        self.cache.delete(f"register_{user.id}")
        cache_exp = minutes_to_seconds(5)
        self.cache.set(f"register_{user.id}", otp, cache_exp)

        task.send_verification_otp.delay([email], otp)

        return Response(
            success=True,
            message="If the email is registered, you will receive an email with the OTP",
            data={"user_id": user.id},
            status_code=200,
        )


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    model = get_user_model()
    cache = Cache()

    def post(self, request):
        """
        Authenticate user and return access token
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(errors=serializer.errors, status_code=400)

        data = serializer.validated_data
        user = self.model.objects.filter(email=data["email"]).first()
        if not user:
            return Response(
                success=False, message="Invalid credentials", status_code=401
            )
        if not user.is_active:
            return Response(
                success=False, message="Account not verified", status_code=400
            )
        if not user.check_password(data["password"]):
            return Response(
                success=False, message="Invalid credentials", status_code=401
            )

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response(
            success=True,
            message="Login successful",
            data={"access_token": access_token},
            status_code=200,
        )


class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = EmailSerializer
    model = get_user_model()
    cache = Cache()

    def post(self, request):
        """
        Request for password reset, send OTP to email and return user id
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(errors=serializer.errors, status_code=400)

        email = serializer.validated_data["email"]
        user = self.model.objects.filter(email=email).first()

        if not user:
            return Response(
                success=True,
                message="If the email is registered, you will receive an email with the OTP",
                status_code=200,
            )

        otp = generate_otp()
        cache_exp = minutes_to_seconds(5)
        self.cache.set(f"forgot_password_{user.id}", otp, cache_exp)

        task.send_verification_otp.delay([email], otp)
        return Response(
            success=True,
            message="If the email is registered, you will receive an email with the OTP",
            data={"user_id": user.id},
            status_code=200,
        )


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    model = get_user_model()
    cache = Cache()

    def patch(self, request):
        """
        Reset password by validating OTP
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(errors=serializer.errors, status_code=400)

        password = serializer.validated_data["password"]
        user_id = serializer.validated_data["user_id"]
        otp = serializer.validated_data["otp"]

        cached_otp = self.cache.get(f"forgot_password_{user_id}")
        if not cached_otp:
            return Response(success=False, message="OTP expired", status_code=400)
        if cached_otp != otp:
            return Response(success=False, message="Invalid OTP", status_code=400)

        user = self.model.objects.filter(id=user_id).first()
        user.set_password(password)
        user.save()
        self.cache.delete(f"forgot_password_{user_id}")

        return Response(
            success=True, message="Password reset successful", status_code=200
        )


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]
    model = get_user_model()

    def patch(self, request):
        """
        Change user password
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(errors=serializer.errors, status_code=400)

        data = serializer.validated_data
        user = self.model.objects.filter(id=request.user.id).first()
        if not user.check_password(data["old_password"]):
            return Response(
                success=False, message="Incorrect password", status_code=400
            )

        user.set_password(data["new_password"])
        user.save()

        return Response(
            success=True, message="Password changed successfully", status_code=200
        )
