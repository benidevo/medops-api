from django.urls import path

from apps.doctors.views import DoctorBulkCreateView, DoctorDetailView, DoctorView

urlpatterns = [
    path("", DoctorView.as_view(), name="doctor-view"),
    path("bulk", DoctorBulkCreateView.as_view(), name="doctor-view"),
    path("<uuid:id>", DoctorDetailView.as_view(), name="doctor-detail-view"),
]
