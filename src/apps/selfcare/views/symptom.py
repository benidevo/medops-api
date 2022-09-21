from rest_framework import generics, permissions

from apps.selfcare.serializers.symptom import SymptomSerializer
from services import Cache, MedicAPI
from utils.response import Response
from utils.utils import hours_to_seconds


class SymptomView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SymptomSerializer
    medic_api = MedicAPI()
    cache = Cache()

    def get(self, request):
        symptoms = self.cache.get("symptoms")

        if symptoms is None:
            symptoms = self.medic_api.list_symptoms()
            cache_exp = hours_to_seconds(24)
            self.cache.set("symptoms", symptoms, cache_exp)

        serializer = self.get_serializer(symptoms, many=True)

        return Response(
            success=True,
            message="User account",
            data=serializer.data,
            status_code=200,
        )
