import uuid

from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

from accounts import logger
from accounts.tasks import send_email
from eventManager.settings import SITE_SCHEMA


class Token(models.Model):
    """Токен"""
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='token',
        null=True
    )
    uid = models.CharField(default=uuid.uuid4, max_length=40)
    email_verified = models.BooleanField(default=False)
    verified_date = models.DateTimeField(verbose_name='Дата и время подтверждения адреса', null=True)
    sendmail_date = models.DateTimeField(verbose_name='Дата и время последней отправки письма подтверждения', null=True)

    def __str__(self):
        return f'{self.owner.email} <email_verified={self.email_verified}> - {str(self.uid)}'

    def get_absolute_url(self):
        return f"{SITE_SCHEMA}://{Site.objects.get_current().domain}{reverse('accounts:confirm', kwargs={'token': self.uid})}"


class Settings(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='settings')
    closing_notice = models.BooleanField(verbose_name='Посылать уведомление о закрытии задачи', default=True)
    comment_notice = models.BooleanField(verbose_name='Посылать уведомление о новых комментариях', default=True)

    def __str__(self):
        return f'Настройки пользователя: {self.user.username}'

    class Meta:
        unique_together = ('user',)


@receiver(signals.post_init, sender=settings.AUTH_USER_MODEL)
def pre_save_user_handler(sender, instance, **kwargs):
    instance.post_init_email = instance.email


@receiver(signals.post_save, sender=settings.AUTH_USER_MODEL)
def post_save_user_handler(sender, instance, **kwargs):
    user_settings, _ = Settings.objects.get_or_create(user=instance)
    logger.debug(f'*** {user_settings} CREATED: {_}')
    if instance.email != instance.post_init_email:
        token, create = Token.objects.get_or_create(owner=instance.id)
        token.email_verified = False
        token.verified_date = None
        msg = {
            'subject': f'🫂 Изменение адрес электронной почты',
            'body': '',
            'recipients': [instance.email],
            'template': 'messages/email_confirm_service.html',
            'check_email_verified': False,
            'confirm_url': token.get_absolute_url(),
        }

        send_email.delay(**msg)
        token.sendmail_date = timezone.now()
        token.save()


