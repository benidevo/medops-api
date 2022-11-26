import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.doctors.models import Doctor

client = APIClient()


doctor_data = {
    "first_name": "Samuel",
    "last_name": "Ogundipe",
    "email": "samuel.ogundipe@example.com",
    "specialty": "Cardiologist",
    "medical_code": "00023",
    "phone": "08012345678",
    "years_of_experience": 5,
}


@pytest.mark.django_db
def get_admin_user():
    admin_user = get_user_model().objects.create_superuser(
        email="admin.one@example.com",
        password="password",
        first_name="Admin",
        last_name="One",
    )

    return admin_user


@pytest.mark.django_db
def get_user():
    regular_user = get_user_model().objects.create_user(
        email="user@example.com",
        password="password",
        first_name="User",
        last_name="One",
        is_active=True,
    )
    return regular_user


@pytest.mark.django_db
def test_create_doctor_validation_error():
    """
    Given that the app is running
    WHEN POST /v1/doctors is called with invalid data and by an authenticated admin user
    THEN the doctor is not created, and a 400 status is returned
    """
    user = get_admin_user()
    client.force_authenticate(user=user)
    email = doctor_data.pop("email")
    doctor_data.update({"email": "invalid_email"})
    response = client.post("/v1/doctors", doctor_data)
    response_data = response.data
    doctor_data.update({"email": email})

    assert response.status_code == 400
    assert response_data["success"] is False
    assert response_data["message"] == "Validation error"
    assert response_data["data"] is None
    assert Doctor.objects.count() == 0


@pytest.mark.django_db
def test_create_doctor__success():
    """
    Given that the app is running
    When POST /v1/doctors is called with valid data and by an authenticated admin user
    Then a new doctor is created, and a 201 status is returned
    """
    admin_user = get_admin_user()
    client.force_authenticate(user=admin_user)
    response = client.post("/v1/doctors", data=doctor_data)
    assert response.status_code == 201
    assert Doctor.objects.count() == 1
    assert Doctor.objects.get().first_name == doctor_data["first_name"]
    assert Doctor.objects.get().last_name == doctor_data["last_name"]
    assert Doctor.objects.get().email == doctor_data["email"]


@pytest.mark.django_db
def test_create_doctor__failure():
    """
    Given that the app is running
    When POST /v1/doctors is called with valid data and by an authenticated regular user
    Then a new doctor is not created, and a 403 status is returned
    """
    user = get_user()
    client.force_authenticate(user=user)
    response = client.post("/v1/doctors", data=doctor_data)
    response_data = response.data

    assert response.status_code == 403
    assert response_data["success"] is False
    assert (
        response_data["message"] == "You do not have permission to perform this action"
    )
    assert Doctor.objects.count() == 0
    assert Doctor.objects.filter(email=doctor_data["email"]).first() is None


@pytest.mark.django_db
def test_create_doctor__failure__no_auth():
    """
    Given that the app is running
    When POST /v1/doctors is called with valid data and by an unauthenticated user
    Then a new doctor is not created, and a 401 status is returned
    """
    client.force_authenticate(user=None)
    response = client.post("/v1/doctors", data=doctor_data)
    assert response.status_code == 401
    assert Doctor.objects.count() == 0
    assert Doctor.objects.filter(email=doctor_data["email"]).first() is None


@pytest.mark.django_db
def test_list_doctors__success():
    """
    Given that the app is running
    When GET /v1/doctors is called by an authenticated admin user
    Then a list of doctors is returned, and a 200 status is returned
    """
    admin_user = get_admin_user()
    Doctor.objects.create(**doctor_data)
    client.force_authenticate(user=admin_user)
    response = client.get("/v1/doctors")
    response_data = response.data

    assert response.status_code == 200
    assert response_data["success"] is True
    assert response_data["message"] == "Doctors retrieved"
    assert response_data["data"][0].get("email") == doctor_data.get("email")
    assert len(response_data.get("data")) == 1
    assert Doctor.objects.count() == 1
    assert Doctor.objects.filter(email=doctor_data["email"]).first() is not None


@pytest.mark.django_db
def test_list_doctors__failure():
    """
    Given that the app is running
    When GET /v1/doctors is called by an authenticated regular user
    Then a list of doctors is not returned, and a 403 status is returned
    """
    user = get_user()
    Doctor.objects.create(**doctor_data)
    client.force_authenticate(user=user)
    response = client.get("/v1/doctors")
    response_data = response.data

    assert response.status_code == 403
    assert response_data["success"] is False
    assert (
        response_data["message"] == "You do not have permission to perform this action"
    )
    assert Doctor.objects.count() == 1
    assert Doctor.objects.filter(email=doctor_data["email"]).first() is not None
    assert Doctor.objects.filter(
        email=doctor_data["email"]
    ).first().email == doctor_data.get("email")


@pytest.mark.django_db
def test_list_doctors__failure__no_auth():
    """
    Given that the app is running
    When GET /v1/doctors is called by an unauthenticated user
    Then a list of doctors is not returned, and a 401 status is returned
    """
    Doctor.objects.create(**doctor_data)
    client.force_authenticate(user=None)
    response = client.get("/v1/doctors")

    assert response.status_code == 401
    assert Doctor.objects.count() == 1
    assert Doctor.objects.filter(email=doctor_data["email"]).first() is not None
    assert Doctor.objects.filter(
        email=doctor_data["email"]
    ).first().email == doctor_data.get("email")
