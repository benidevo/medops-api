from rest_framework import generics, permissions

from apps.doctors.models import Doctor
from apps.doctors.serializers import DoctorSerializer
from apps.selfcare.serializers.diagnosis import (
    DiagnosisSerializer,
    GetDiagnosisSerializer,
)
from services import MedicAPI
from utils.response import Response


class DiagnosisView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetDiagnosisSerializer
    medic_api = MedicAPI()

    def doctors_serializer(self, doctors):
        return DoctorSerializer(doctors, many=True)

    def post(self, request):
        """
        Get diagnosis report and a list of recommended doctors based on the provided symptoms IDs
        """
        user = request.user

        if not user.profile.is_complete():
            return Response(
                success=False,
                message="Incomplete profile",
                status_code=400,
                data=None,
            )

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status_code=400,
                success=False,
                errors=serializer.errors,
            )
        symptoms = serializer.validated_data["symptom_ids"]
        yob = user.profile.year_of_birth()
        gender = "male" if user.profile.gender == "M" else "female"

        diagnosis = self.medic_api.get_diagnosis(gender, yob, symptoms)

        result = [obj for obj in diagnosis if obj["Issue"]["Accuracy"] >= 50]
        serializer = DiagnosisSerializer(result, many=True)

        specialty = [
            spec["Name"] for obj in serializer.data for spec in obj["Specialisation"]
        ]

        for obj in serializer.data:
            obj.pop("Specialisation")

        doctors = Doctor.objects.filter(specialty__in=specialty)
        doctors_serializer = self.doctors_serializer(doctors)
        response_data = {"result": serializer.data, "doctors": doctors_serializer.data}

        return Response(
            success=True,
            message="Diagnosis results",
            data=response_data,
            status_code=200,
        )
