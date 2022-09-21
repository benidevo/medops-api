from django.urls import path

from apps.selfcare.views.diagnosis import DiagnosisView
from apps.selfcare.views.symptom import SymptomView

urlpatterns = [
    path("symptoms", SymptomView.as_view(), name="symptoms"),
    path("diagnosis", DiagnosisView.as_view(), name="diagnosis"),
]
