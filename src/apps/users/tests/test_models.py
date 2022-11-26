import pytest
from django.contrib.auth import get_user_model

from apps.users.models import Profile


@pytest.mark.django_db
def test_create_user():
    """
    GIVEN that the app is running
    WHEN a user is created
    THEN a profile is also created for that user
    """
    user = get_user_model().objects.create_user(
        first_name="John",
        last_name="Doe",
        email="example@gmail.com",
        password="password",
    )
    user_id = user.pkid
    profile = Profile.objects.filter(user_id=user_id).first()

    assert profile is not None
    assert profile.user_id == user_id
    assert user.is_active == False
