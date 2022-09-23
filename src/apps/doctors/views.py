import csv
import os
import random
from uuid import uuid4 as uuid

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import generics, permissions

from apps.doctors.models import Doctor
from apps.doctors.serializers import DoctorSerializer, DoctorsUploadSerializer
from utils.response import Response


class DoctorView(generics.GenericAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]
    model = Doctor

    def post(self, request):
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


class DoctorBulkCreateView(generics.GenericAPIView):
    serializer_class = DoctorsUploadSerializer
    permission_classes = [permissions.IsAuthenticated]
    model = Doctor

    def post(self, request):
        doc = request.FILES.get("doc")
        if not doc:
            return Response(
                success=False,
                message="File not found",
                status_code=400,
            )
        unique_id = str(uuid())
        file_name = f"{unique_id}_{doc.name}"
        path = default_storage.save(f"tmp/{file_name}", ContentFile(doc.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)

        with open(f"{tmp_file}") as file:
            reader = csv.reader(file)
            next(reader)  # Advance past the header

            for row in reader:
                self.model.objects.update_or_create(
                    first_name=row[1],
                    last_name=row[2],
                    email=row[3],
                    specialty=row[4],
                    phone=row[5],
                    medical_code=row[6],
                    years_of_experience=row[7],
                )

        os.remove(tmp_file)
        return Response(
            success=True,
            message="Doctors created",
            status_code=201,
        )


class Load(generics.GenericAPIView):
    serializer_class = None
    model = Doctor

    def get(self, request):
        # generate random medical specialty
        specialty = [
            "Pulmonology",
            "Dermatology",
            "Hematology",
            "Nephrology",
            "Anaesthesiology",
            "Ophthalmology",
            "Orthopaedics",
            "Obstetrics and gynaecology",
            "Psychiatry",
            "Infectious diseases",
            "Rehabilitation medicine",
            "Surgery",
            "Pediatrics",
            "Respiratory medicine",
            "Radiology",
            "Otolaryngology",
            "Orthopedics",
            "Geriatrics",
            "Vascular surgery",
            "Neurology",
            "Dentistry",
            "Gastroenterology",
            "Rheumatology",
            "Endocrinology",
            "Cardiology",
            "Urology",
            "Oncology",
            "General practice",
            "Clinical pharmacology",
            "Internal medicine",
            "Allergology",
        ]
        doctors = self.model.objects.all()
        for doctor in doctors:
            doctor.specialty = random.choice(specialty)
            doctor.save()

        return Response(
            success=True,
            message="Doctors loaded",
            status_code=201,
        )
