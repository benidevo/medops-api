from rest_framework import generics, permissions

from apps.doctors.models import Doctor
from apps.doctors.serializers import DoctorSerializer
from utils.response import Response


class DoctorDetailView(generics.GenericAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    model = Doctor

    def get(self, request, id):
        """Retrieve a doctor by id"""
        queryset = self.model.objects.filter(id=id).first()
        if not queryset:
            return Response(
                success=False,
                message="Doctor not found",
                status_code=404,
            )
        serializer = self.get_serializer(queryset)
        return Response(
            success=True,
            message="Doctor retrieved",
            data=serializer.data,
            status_code=200,
        )

    def patch(self, request, id):
        """Update a doctor by id"""
        queryset = self.model.objects.filter(id=id).first()
        if not queryset:
            return Response(
                success=False,
                message="Doctor not found",
                status_code=404,
            )
        serializer = self.get_serializer(queryset, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                success=False,
                errors=serializer.errors,
                status_code=400,
            )
        serializer.save()

        return Response(
            success=True,
            message="Doctor updated",
            data=serializer.data,
            status_code=200,
        )

    def delete(self, request, id):
        """Delete a doctor by id"""
        queryset = self.model.objects.filter(id=id).first()
        if not queryset:
            return Response(
                success=False,
                message="Doctor not found",
                status_code=404,
            )
        queryset.delete()
        return Response(
            success=True,
            message="Doctor deleted",
            status_code=200,
        )
