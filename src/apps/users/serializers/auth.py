from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8)

    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name")
        extra_kwargs = {"password": {"write_only": True}}


class VerifyAccountSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    otp = serializers.CharField()


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class LoginSerializer(EmailSerializer):
    password = serializers.CharField(min_length=8)


class ResetPasswordSerializer(VerifyAccountSerializer):
    password = serializers.CharField(min_length=8)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=8)
    new_password = serializers.CharField(min_length=8)
