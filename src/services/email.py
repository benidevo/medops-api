import logging
import os
from pathlib import Path

from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logger = logging.getLogger(__name__)


class EmailService:
    template_dir = Path(__file__).resolve().parent.parent / "templates"

    def __init__(self):
        self.client = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))

    def send_verification_mail(self, recipient_list, otp):
        content = self.template("verification-email.html")
        content = content.replace("000000", otp)

        self._send_mail("Verify your account", recipient_list, content)

    def template(self, template_name):
        with open(f"{self.template_dir}/{template_name}", "r") as file:
            html_as_string = file.read()
        return html_as_string

    def _send_mail(self, subject, recipient_list, content):
        message = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=recipient_list,
            subject=subject,
            html_content=content,
        )
        try:
            self.client.send(message)
        except Exception as e:
            logger.error(e)
