from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def guest_email_validator(value):
    user = User.objects.filter(email=value)
    if user:
        raise ValidationError(
            _("User with %(value)s is already registered"),
            params={"value": value},
        )