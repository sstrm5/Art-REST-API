from celery import shared_task


@shared_task
def send_code_to_email_task(email: str, code: str, first_name: str):
    from core.apps.customers.services.senders import MailSenderService
    sender_service = MailSenderService()
    sender_service.send_code(email=email, code=code, first_name=first_name)
