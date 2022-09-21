from rest_framework import generics, permissions

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

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status_code=400,
                success=False,
                message="Invalid data",
                errors=serializer.errors,
            )
        data = serializer.validated_data

        diagnosis = self.medic_api.get_diagnosis(data)

        serializer = DiagnosisSerializer(diagnosis, many=True)

        return Response(
            success=True,
            message="Diagnosis results",
            data=serializer.data,
            status_code=200,
        )
