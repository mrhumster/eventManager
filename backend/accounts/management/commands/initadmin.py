import os

from django.contrib.auth.models import User
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@server.local")
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin")
        if User.objects.count() == 0:
                admin = User.objects.create_superuser(
                    email=email, username=username, password=password,
                    first_name='Super', last_name='Admin')
                admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')