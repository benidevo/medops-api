from rest_framework import generics, permissions

from apps.doctors.models import Doctor
from apps.doctors.serializers import DoctorSerializer
from utils.response import Response


class DoctorView(generics.GenericAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    model = Doctor

    def post(self, request):
        """
        Create a doctor
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                success=False,
                errors=serializer.errors,
                status_code=400,
            )
        serializer.save()

        return Response(
            success=True,
            message="Doctor created",
            data=serializer.data,
            status_code=201,
        )

    def get(self, request):
        """Retrieve a list of doctors"""
        queryset = self.model.objects.all()
        serializer = self.get_serializer(queryset, many=True)

        return Response(
            success=True,
            message="Doctors retrieved",
            data=serializer.data,
            status_code=200,
        )
