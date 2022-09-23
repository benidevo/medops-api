from celery import shared_task

from services import EmailService

mail_client = EmailService()


@shared_task
def send_verification_otp(recipient_list, otp):
    mail_client.send_verification_mail(recipient_list, otp)
