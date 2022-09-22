from uuid import uuid4 as uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Doctor(models.Model):
    pkid = models.BigAutoField(primary_key=True)
    id = models.UUIDField(default=uuid, editable=False, unique=True)
    first_name = models.CharField(max_length=50, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=50, verbose_name=_("Last Name"))
    email = models.EmailField(verbose_name=_("Email"), max_length=255, unique=True)
    specialty = models.CharField(max_length=100, verbose_name=_("Specialty"))
    medical_code = models.CharField(
        max_length=100, unique=True, verbose_name=_("Medical Code")
    )
    phone = models.CharField(max_length=255, verbose_name=_("Phone"))
    years_of_experience = models.IntegerField(verbose_name=_("Years of Experience"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("doctor")
        verbose_name_plural = _("doctors")
        ordering = ["-created_at", "-updated_at"]

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
