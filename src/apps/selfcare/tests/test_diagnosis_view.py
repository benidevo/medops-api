import pytest
from rest_framework.test import APIClient

from apps.doctors.tests.test_doctor_view import get_completed_user_profile, get_user

client = APIClient()


@pytest.mark.django_db
def get_symptoms():
    user = get_user()
    client.force_authenticate(user=user)
    response = client.get("/v1/selfcare/symptoms")
    response_data = response.data.get("data")

    return response_data[0].get("id"), response_data[1].get("id")


@pytest.mark.django_db
def test_get_diagnosis_failure_no_auth():
    """
    GIVEN that the app is running
    WHEN POST /v1/selfcare/diagnosis is called by an unauthenticated user
    THEN a 401 status is returned
    """
    symptoms = get_symptoms()
    payload = {"symptom_ids": [symptoms[0], symptoms[1]]}
    client.force_authenticate(user=None)
    response = client.post("/v1/selfcare/diagnosis", payload)
    response_data = response.data

    assert response.status_code == 401
    assert response_data.get("success") is False
    assert (
        response_data.get("message") == "Authentication credentials were not provided."
    )
    assert response_data.get("data") is None


@pytest.mark.django_db
def test_get_diagnosis_failure_validation_error():
    """
    GIVEN that the app is running
    WHEN POST /v1/selfcare/diagnosis is called with invalid payload
    THEN a 400 status code is returned and validation error is returned
    """
    user = get_completed_user_profile()
    client.force_authenticate(user=user)
    payload = {"symptom_ids": "invalid"}
    response = client.post("/v1/selfcare/diagnosis", payload)
    response_data = response.data

    response2 = client.post("/v1/selfcare/diagnosis", {})
    response_data2 = response2.data

    assert response.status_code == 400
    assert response_data.get("success") is False
    assert response_data.get("message") == "Validation error"
    assert response_data.get("data") is None
    assert response2.status_code == 400
    assert response_data2.get("success") is False
    assert response_data2.get("message") == "Validation error"
    assert response_data2.get("data") is None


@pytest.mark.django_db
def test_get_diagnosis_failure_incomplete_profile():
    """
    GIVEN that the app is running
    WHEN POST /v1/selfcare/diagnosis is called by a user with incomplete profile
    THEN a 400 status code is returned
    """
    user = get_user()
    client.force_authenticate(user=user)
    symptoms = get_symptoms()
    payload = {"symptom_ids": [symptoms[0], symptoms[1]]}
    response = client.post("/v1/selfcare/diagnosis", payload)
    response_data = response.data

    assert response.status_code == 400
    assert response_data.get("success") is False
    assert response_data.get("message") == "Incomplete profile"
    assert response_data.get("data") is None
