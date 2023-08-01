from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import get_template

from accounts import logger
from eventManager.settings import EMAIL_HOST_USER


@shared_task
def send_email(subject, template, recipients, check_email_verified=True,  **kwargs):
    html_body = get_template(template).render(kwargs)
    if check_email_verified:
        to = [email for email in recipients if User.objects.get(email=email).token.first().email_verified]
    else:
        to = list(recipients)
    if to:
        msg = EmailMessage(
            subject,
            html_body,
            EMAIL_HOST_USER,
            to
        )
        msg.content_subtype = "HTML"
        msg.send()
        return f'[{", ".join(msg.to)}] Письмо поставлено в очередь.'
    else:
        logger.debug(f'Письмо не отправлено, т.к. список адресатов пуст.')

