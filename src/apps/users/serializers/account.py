from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "avatar", "age", "gender"]


class UserAccountSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "profile",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "email": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def update(self, instance, validated_data):
        print(validated_data)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        profile_data = validated_data.pop("profile", None)
        if profile_data:
            profile = instance.profile
            profile.avatar = profile_data.get("avatar", profile.avatar)
            profile.age = profile_data.get("age", profile.age)
            profile.gender = profile_data.get("gender", profile.gender)
            profile.save()
        instance.save()
        return instance
