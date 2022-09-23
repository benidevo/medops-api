from rest_framework import generics, permissions

from apps.selfcare.serializers.symptom import SymptomSerializer
from services import Cache, MedicAPI
from utils.response import Response
from utils.utils import days_to_seconds


class SymptomView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SymptomSerializer
    medic_api = MedicAPI()
    cache = Cache()

    def get(self, request):
        """
        Retrieve a list of symptoms from the medic api
        """
        symptoms = self.cache.get("symptoms")

        if symptoms is None:
            symptoms = self.medic_api.list_symptoms()
            cache_exp = days_to_seconds(2)
            self.cache.set("symptoms", symptoms, cache_exp)

        serializer = self.get_serializer(symptoms, many=True)

        return Response(
            success=True,
            message="Symptoms retrieved",
            data=serializer.data,
            status_code=200,
        )
