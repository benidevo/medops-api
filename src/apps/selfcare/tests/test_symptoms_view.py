import pytest
from rest_framework.test import APIClient

from apps.doctors.tests.test_doctor_view import get_user


@pytest.mark.django_db
def test_list_symptoms():
    """
    Given that the app is running
    WHEN GET /v1/symptoms is called by an authenticated user
    THEN the symptoms are retrieved, and a 200 status is returned
    """
    user = get_user()
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get("/v1/selfcare/symptoms")
    response_data = response.data

    assert response.status_code == 200
    assert response_data["success"] is True
    assert response_data["message"] == "Symptoms retrieved"
    assert len(response_data["data"]) > 0
    assert isinstance(response_data["data"], list)
    assert isinstance(response_data["data"][0], dict)
    assert response_data["data"][0].keys() == {"id", "name"}


@pytest.mark.django_db
def test_list_symptoms_failure_not_authenticated():
    """
    Given that the app is running
    WHEN GET /v1/symptoms is called by an unauthenticated user
    THEN a 401 status is returned
    """
    client = APIClient()
    client.force_authenticate(user=None)
    response = client.get("/v1/selfcare/symptoms")
    response_data = response.data

    assert response.status_code == 401
    assert response_data["message"] == "Authentication credentials were not provided."
    assert response_data["success"] is False
    assert response_data["data"] is None
