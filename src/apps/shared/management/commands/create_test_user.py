import logging

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from apps.users.models import Profile

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Create a test user"

    def handle(self, *args, **options):
        logger.info("Creating a test user")
        try:
            if get_user_model().objects.filter(email="john@example.com").exists():
                logger.info("Test user already exists")
                return
            user = get_user_model().objects.create_user(
                email="john@example.com",
                first_name="John",
                last_name="Doe",
                password="TestPassword",
                is_active=True,
            )
            Profile.objects.filter(user=user).update(age=40, gender="M")
            logger.info("User created")
        except Exception as e:
            logger.error(e)
            raise CommandError("Failed to create a test user")
