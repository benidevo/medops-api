import pytest
from django.contrib.auth import get_user_model

user = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "johndoe@example.com",
    "password": "password",
}


@pytest.mark.django_db
def test_user_registration__success(client):
    """
    GIVEN that the app is running
    WHEN /v1/users/auth/register is called with valid data
    THEN a new user is created, and a 201 status is returned
    """
    response = client.post("/v1/users/auth/register", data=user)
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
    user.update({"email": "invalid_email"})
    response = client.post("/v1/users/auth/register", data=user)
    response_data = response.json()

    assert response.status_code == 400
    assert response_data["success"] == False
    assert len(get_user_model().objects.all()) == 0
