import pytest
from rest_framework.test import APIClient

from apps.doctors.models import Doctor

from .test_doctor_view import doctor_data, get_admin_user, get_user

client = APIClient()

UPDATED_DOCTOR_DATA = {
    "first_name": "John",
    "Specialty": "Surgeon",
}


@pytest.mark.django_db
def create_doctor():
    doctor = Doctor.objects.create(**doctor_data)
    return doctor


@pytest.mark.django_db
def test_get_doctor_by_id():
    """
    Given that the app is running
    WHEN GET /v1/doctors/<id> is called with a valid id and by an authenticated admin user
    THEN the doctor is retrieved, and a 200 status is returned
    """
    doctor = create_doctor()
    user = get_admin_user()
    client.force_authenticate(user=user)
    response = client.get(f"/v1/doctors/{doctor.id}")
    response_data = response.data

    assert response.status_code == 200
    assert response_data["success"] is True
    assert Doctor.objects.count() == 1
    assert Doctor.objects.filter(email=doctor_data["email"]).first() is not None
    assert response_data["data"].get("email") == doctor.email


@pytest.mark.django_db
def test_get_doctor_by_id__failure():
    """
    Given that the app is running
    WHEN GET /v1/doctors/<id> is called with a valid id and by an authenticated regular user
    THEN the doctor is not retrieved, and a 403 status is returned
    """
    doctor = create_doctor()
    user = get_user()
    client.force_authenticate(user=user)
    response = client.get(f"/v1/doctors/{doctor.id}")
    response_data = response.data

    assert response.status_code == 403
    assert response_data["success"] is False
    assert (
        response_data["message"] == "You do not have permission to perform this action"
    )
    assert response_data["data"] is None
    assert Doctor.objects.count() == 1
    assert Doctor.objects.filter(email=doctor_data["email"]).first() is not None
    assert (
        Doctor.objects.filter(email=doctor_data["email"]).first().email == doctor.email
    )


@pytest.mark.django_db
def test_get_doctor_by_id__failure__no_auth():
    """
    Given that the app is running
    WHEN GET /v1/doctors/<id> is called with a valid id and by an unauthenticated user
    THEN the doctor is not retrieved, and a 401 status is returned
    """
    doctor = create_doctor()
    client.force_authenticate(user=None)
    response = client.get(f"/v1/doctors/{doctor.id}")
    response_data = response.data

    assert response.status_code == 401
    assert response_data["success"] is False
    assert response_data["message"] == "Authentication credentials were not provided."
    assert response_data["data"] is None
    assert Doctor.objects.count() == 1
    assert Doctor.objects.filter(email=doctor_data["email"]).first() is not None
    assert (
        Doctor.objects.filter(email=doctor_data["email"]).first().email == doctor.email
    )


@pytest.mark.django_db
def test_update_doctor_validation_error():
    """
    Given that the app is running
    WHEN PATCH /v1/doctors/<id> is called with an invalid payload and by an authenticated admin user
    THEN the doctor is not updated, and a 400 status is returned
    """
    doctor = create_doctor()
    user = get_admin_user()
    client.force_authenticate(user=user)
    UPDATED_DOCTOR_DATA.update({"email": "invalid_email"})
    response = client.patch(f"/v1/doctors/{doctor.id}", data=UPDATED_DOCTOR_DATA)
    response_data = response.data
    UPDATED_DOCTOR_DATA.pop("email")

    assert response.status_code == 400
    assert response_data["success"] is False
    assert response_data["message"] == "Validation error"
    assert response_data["data"] is None
    assert Doctor.objects.count() == 1
    assert Doctor.objects.filter(email=doctor_data["email"]).first() is not None
    assert (
        Doctor.objects.filter(email=doctor_data["email"]).first().email == doctor.email
    )


@pytest.mark.django_db
def test_update_doctor():
    """
    Given that the app is running
    WHEN PATCH /v1/doctors/<id> is called with a valid id and data and by an authenticated admin user
    THEN the doctor is updated, and a 200 status is returned
    """
    doctor = create_doctor()
    user = get_admin_user()
    client.force_authenticate(user=user)
    response = client.patch(f"/v1/doctors/{doctor.id}", data=UPDATED_DOCTOR_DATA)
    response_data = response.data
    updated_doctor = Doctor.objects.filter(id=doctor.id).first()

    assert response.status_code == 200
    assert response_data.get("success") is True
    assert Doctor.objects.count() == 1
    assert updated_doctor.first_name == UPDATED_DOCTOR_DATA.get("first_name")
    assert updated_doctor.last_name == doctor_data.get("last_name")
    assert updated_doctor.specialty == doctor_data.get("specialty")


@pytest.mark.django_db
def test_update_doctor_failure():
    """
    Given that the app is running
    WHEN PATCH /v1/doctors/<id> is called with a valid id and valid payload by an authenticated regular user
    THEN the doctor is not updated, and a 403 status is returned
    """
    doctor = create_doctor()
    user = get_user()
    client.force_authenticate(user=user)
    response = client.patch(f"/v1/doctors/{doctor.id}", data=UPDATED_DOCTOR_DATA)
    response_data = response.data
    updated_doctor = Doctor.objects.filter(id=doctor.id).first()

    assert response.status_code == 403
    assert response_data.get("success") is False
    assert (
        response_data.get("message")
        == "You do not have permission to perform this action"
    )
    assert Doctor.objects.count() == 1
    assert updated_doctor.first_name == doctor_data.get("first_name")
    assert updated_doctor.last_name == doctor_data.get("last_name")
    assert updated_doctor.specialty == doctor_data.get("specialty")


@pytest.mark.django_db
def test_update_doctor_failure__no_auth():
    """
    Given that the app is running
    WHEN PATCH /v1/doctors/<id> is called with a valid id and by an unauthenticated user
    THEN the doctor is not updated, and a 401 status is returned
    """
    doctor = create_doctor()
    client.force_authenticate(user=None)
    response = client.patch(f"/v1/doctors/{doctor.id}", data=UPDATED_DOCTOR_DATA)
    response_data = response.data
    updated_doctor = Doctor.objects.filter(id=doctor.id).first()

    assert response.status_code == 401
    assert response_data.get("success") is False
    assert (
        response_data.get("message") == "Authentication credentials were not provided."
    )
    assert Doctor.objects.count() == 1
    assert updated_doctor.first_name == doctor_data.get("first_name")
    assert updated_doctor.last_name == doctor_data.get("last_name")
    assert updated_doctor.specialty == doctor_data.get("specialty")


@pytest.mark.django_db
def test_delete_doctor():
    """
    Given that the app is running
    WHEN DELETE /v1/doctors/<id> is called with a valid id and by an authenticated admin user
    THEN the doctor is deleted, and a 200 status is returned
    """
    doctor = create_doctor()
    user = get_admin_user()
    client.force_authenticate(user=user)
    response = client.delete(f"/v1/doctors/{doctor.id}")
    response_data = response.data

    assert response.status_code == 200
    assert response_data.get("success") is True
    assert Doctor.objects.count() == 0
    assert Doctor.objects.filter(email=doctor_data["email"]).first() is None


@pytest.mark.django_db
def test_delete_doctor_failure():
    """
    Given that the app is running
    WHEN DELETE /v1/doctors/<id> is called with a valid id and by an authenticated regular user
    THEN the doctor is not deleted, and a 403 status is returned
    """
    doctor = create_doctor()
    user = get_user()
    client.force_authenticate(user=user)
    response = client.delete(f"/v1/doctors/{doctor.id}")
    response_data = response.data

    assert response.status_code == 403
    assert response_data.get("success") is False
    assert (
        response_data.get("message")
        == "You do not have permission to perform this action"
    )
    assert Doctor.objects.count() == 1
    assert Doctor.objects.filter(email=doctor_data["email"]).first() is not None
    assert (
        Doctor.objects.filter(email=doctor_data["email"]).first().email == doctor.email
    )


@pytest.mark.django_db
def test_delete_doctor_failure__no_auth():
    """
    Given that the app is running
    WHEN DELETE /v1/doctors/<id> is called with a valid id and by an unauthenticated user
    THEN the doctor is not deleted, and a 401 status is returned
    """
    doctor = create_doctor()
    client.force_authenticate(user=None)
    response = client.delete(f"/v1/doctors/{doctor.id}")
    response_data = response.data

    assert response.status_code == 401
    assert response_data.get("success") is False
    assert (
        response_data.get("message") == "Authentication credentials were not provided."
    )
    assert Doctor.objects.count() == 1
    assert Doctor.objects.filter(email=doctor_data["email"]).first() is not None
    assert (
        Doctor.objects.filter(email=doctor_data["email"]).first().email == doctor.email
    )
