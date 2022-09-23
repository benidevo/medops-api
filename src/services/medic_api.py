import requests
from django.conf import settings


class MedicAPI:
    def __init__(self):
        self.base_url = settings.MEDIC_API_URL
        self.token = settings.MEDIC_API_TOKEN

    def list_symptoms(self):
        url = "{}/symptoms?token={}&format=json&language=en-gb".format(
            self.base_url, self.token
        )

        response = requests.get(url)
        return response.json()

    def get_diagnosis(self, gender, yob, symptoms):
        url = "{}/diagnosis?symptoms={}&gender={}&year_of_birth={}&token={}&format=json&language=en-gb".format(
            self.base_url, symptoms, gender, yob, self.token
        )

        response = requests.get(url)
        return response.json()
