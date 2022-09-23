import csv
import logging
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from apps.doctors.models import Doctor

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Load Doctors from CSV file"

    def handle(self, *args, **options):
        logger.info("Loading doctors from CSV file")
        try:
            document = (
                Path(__file__).resolve().parent.parent.parent.parent.parent
                / "data"
                / "doctors-data.csv"
            )
            with open(document) as file:
                reader = csv.reader(file)
                next(reader)

                for row in reader:
                    Doctor.objects.update_or_create(
                        first_name=row[1],
                        last_name=row[2],
                        email=row[3],
                        specialty=row[4],
                        phone=row[5],
                        medical_code=row[6],
                        years_of_experience=row[7],
                    )

            logger.info("Doctors loaded")
        except Exception as e:
            logger.error(e)
            raise CommandError("Failed to load doctors")
