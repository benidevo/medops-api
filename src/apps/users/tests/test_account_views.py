import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.users.models import Profile

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
def test_retrieve_user_account():
    """
    GIVEN that the app is running
    WHEN /v1/users/account is called with a GET request
    THEN the account of the current user and a 200 status code is returned
    """
    user_data = get_user_data()
    user_data.update({"is_active": True})
    user = get_user_model().objects.create_user(**user_data)

    access_token = get_user_token(user_data["email"], user_data["password"])

    response = client.get(
        "/v1/users/account", HTTP_AUTHORIZATION=f"Bearer {access_token}"
    )
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["success"] == True
    assert response_data["message"] == "Retrieved user account"
    assert response_data["data"]["id"] == str(user.id)
    assert response_data["data"]["email"] == user_data["email"]


@pytest.mark.django_db
def test_update_user_account():
    """
    GIVEN that the app is running
    WHEN /v1/users/account is called with a PATCH request
    THEN the account of the current user is updated and a 200 status code is returned
    """
    user_data = get_user_data()
    user_data.update({"is_active": True})
    user = get_user_model().objects.create_user(**user_data)

    access_token = get_user_token(user_data["email"], user_data["password"])

    new_user_data = {
        "first_name": "Jane",
        "last_name": "Doe",
        "profile": {"age": 25, "gender": "M"},
    }

    response = client.patch(
        "/v1/users/account",
        data=new_user_data,
        HTTP_AUTHORIZATION=f"Bearer {access_token}",
        format="json",
    )
    response_data = response.json()

    user = get_user_model().objects.get(id=user.id)
    profile = Profile.objects.get(user=user)

    assert response.status_code == 200
    assert response_data["success"] == True
    assert response_data["message"] == "User account updated"
    assert user.first_name == new_user_data["first_name"]
    assert user.last_name == new_user_data["last_name"]
    assert new_user_data["profile"]["age"] == profile.age
    assert new_user_data["profile"]["gender"] == profile.gender


@pytest.mark.django_db
def test_delete_user_account():
    """
    GIVEN that the app is running
    WHEN /v1/users/account is called with a DELETE request
    THEN the account of the current user is deleted and a 200 status code is returned
    """
    user_data = get_user_data()
    user_data.update({"is_active": True})
    user = get_user_model().objects.create_user(**user_data)

    access_token = get_user_token(user_data["email"], user_data["password"])

    response = client.delete(
        "/v1/users/account", HTTP_AUTHORIZATION=f"Bearer {access_token}"
    )

    response_data = response.json()

    assert response.status_code == 200
    assert response_data["success"] == True
    assert response_data["message"] == "Account deleted"
    assert get_user_model().objects.filter(id=user.id).count() == 0
