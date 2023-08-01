# accounts/backends.py
from django.contrib.auth.backends import ModelBackend, UserModel
from django.contrib.auth.models import User


class CaseInsensitiveModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username__iexact=username)
            if user.check_password(password):
                return user
            else:
                return None
        except UserModel().DoesNotExist:
            return None
