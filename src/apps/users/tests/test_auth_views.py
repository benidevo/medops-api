import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from services import Cache

client = APIClient()


def get_user_data():
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@example.com",
        "password": "password",
    }
    return user_data


def get_user_token(email, password):

    data = {"email": email, "password": password}
    response = client.post("/v1/users/auth/login", data=data)
    response_data = response.json()

    return response_data["data"]["accessToken"]


@pytest.mark.django_db
def test_user_registration__success(client):
    """
    GIVEN that the app is running
    WHEN /v1/users/auth/register is called with valid data
    THEN a new user is created, and a 201 status is returned
    """
    response = client.post("/v1/users/auth/register", data=get_user_data())
    response_data = response.json()
    user_id = response_data["data"]["userId"]

    assert response.status_code == 201
    assert response_data["success"] == True
    assert isinstance(user_id, str)
    assert len(user_id) > 10
    assert get_user_model().objects.filter(id=user_id).exists() == True


@pytest.mark.django_db
def test_user_registration__failure(client):
    """
    GIVEN that the app is running
    WHEN /v1/users/auth/register is called with invalid data
    THEN a new user is not created, and a 400 status code is returned
    """
    user_data = get_user_data()
    user_data["email"] = "invalid_email"

    response = client.post("/v1/users/auth/register", data=user_data)
    response_data = response.json()

    assert response.status_code == 400
    assert response_data["success"] == False
    assert len(get_user_model().objects.all()) == 0


@pytest.mark.django_db
def test_verify_account():
    """
    GIVEN that the app is running
    WHEN /v1/users/auth/verify is called with valid data
    THEN the user is verified, and a 200 status code is returned
    """
    user_data = get_user_data()
    user = get_user_model().objects.create_user(**user_data)

    cache = Cache()
    cache.set(f"register_{user.id}", "123456", 60)
    data = {"userId": str(user.id), "otp": "123456"}
    response = client.patch("/v1/users/auth/verify", data=data)
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["success"] == True
    assert response_data["message"] == "Account verified"


@pytest.mark.django_db
def test_resend_verification_otp():
    """
    GIVEN that the app is running
    WHEN /v1/users/auth/resend-otp is called with valid data
    THEN the user receives a new OTP, and a 200 status code is returned
    """
    user_data = get_user_data()
    user = get_user_model().objects.create_user(**user_data)

    data = {"email": user.email}
    response = client.post("/v1/users/auth/resend-otp", data=data)
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["success"] == True
    assert (
        response_data["message"]
        == "If the email is registered, you will receive an email with the OTP"
    )


@pytest.mark.django_db
def test_login():
    """
    GIVEN that the app is running
    WHEN /v1/users/auth/login is called with valid data
    THEN the access token and a 200 status code is returned
    """
    user_data = get_user_data()
    user_data.update({"is_active": True})
    user = get_user_model().objects.create_user(**user_data)

    data = {"email": user.email, "password": user_data["password"]}
    response = client.post("/v1/users/auth/login", data=data)
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["success"] == True
    assert response_data["message"] == "Login successful"
    assert "accessToken" in response_data["data"]
    assert response_data["data"]["accessToken"] != None


@pytest.mark.django_db
def test_change_password():
    """
    GIVEN that the app is running
    WHEN /v1/users/auth/change-password is called with valid data
    THEN the password is changed, and a 200 status code is returned
    """
    user_data = get_user_data()
    user_data.update({"is_active": True})
    user = get_user_model().objects.create_user(**user_data)

    data = {
        "oldPassword": user_data["password"],
        "newPassword": "new_password",
    }
    access_token = get_user_token(user.email, user_data["password"])
    response = client.patch(
        "/v1/users/auth/change-password",
        data=data,
        HTTP_AUTHORIZATION=f"Bearer {access_token}",
    )
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["success"] == True
    assert response_data["message"] == "Password changed successfully"


@pytest.mark.django_db
def test_forgot_password():
    """
    GIVEN that the app is running
    WHEN /v1/users/auth/forgot-password is called with valid data
    THEN the user receives an email with the OTP, and a 200 status code is returned
    """
    user_data = get_user_data()
    user_data.update({"is_active": True})
    user = get_user_model().objects.create_user(**user_data)

    data = {"email": user.email}
    response = client.post("/v1/users/auth/forgot-password", data=data)
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["success"] == True
    assert (
        response_data["message"]
        == "If the email is registered, you will receive an email with the OTP"
    )


@pytest.mark.django_db
def test_reset_password():
    """
    GIVEN that the app is running
    WHEN /v1/users/auth/reset-password is called with valid data
    THEN the password is reset, and a 200 status code is returned
    """
    user_data = get_user_data()
    user_data.update({"is_active": True})
    user = get_user_model().objects.create_user(**user_data)

    cache = Cache()
    cache.set(f"forgot_password_{user.id}", "123456", 60)
    data = {
        "userId": str(user.id),
        "otp": "123456",
        "password": "new_password",
    }
    response = client.patch("/v1/users/auth/reset-password", data=data)
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["success"] == True
    assert response_data["message"] == "Password reset successful"
