from rest_framework import generics, permissions

from apps.doctors.models import Doctor
from apps.doctors.serializers import DoctorSerializer
from utils.response import Response


class DoctorView(generics.GenericAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]
    model = Doctor

    def post(self, request):
        """
        Create a doctor
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                success=False,
                data=serializer.errors,
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


class DoctorDetailView(generics.GenericAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]
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
                data=serializer.errors,
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
