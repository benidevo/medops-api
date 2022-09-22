from rest_framework import serializers

from apps.doctors.models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "medical_code",
            "specialty",
            "years_of_experience",
            "created_at",
            "updated_at",
        ]


class DoctorsUploadSerializer(serializers.Serializer):
    doc = serializers.FileField()
