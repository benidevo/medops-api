# Generated by Django 4.1.1 on 2022-09-22 01:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Doctor",
            fields=[
                ("pkid", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                (
                    "first_name",
                    models.CharField(max_length=50, verbose_name="First Name"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=50, verbose_name="Last Name"),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=255, unique=True, verbose_name="Email"
                    ),
                ),
                (
                    "specialty",
                    models.CharField(max_length=100, verbose_name="Specialty"),
                ),
                (
                    "medical_code",
                    models.CharField(
                        max_length=100, unique=True, verbose_name="Medical Code"
                    ),
                ),
                ("phone", models.CharField(max_length=255, verbose_name="Phone")),
                (
                    "years_of_experience",
                    models.IntegerField(verbose_name="Years of Experience"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated At"),
                ),
            ],
            options={
                "verbose_name": "doctor",
                "verbose_name_plural": "doctors",
                "ordering": ["-created_at", "-updated_at"],
            },
        ),
    ]
