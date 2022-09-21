from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SelfcareConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.selfcare"
    verbose_name = _("Selfcare")
