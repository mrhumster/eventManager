import os

from django.contrib.auth.models import User, Group, Permission
from django.contrib.sites.models import Site
from django.core.management import BaseCommand

from accounts import logger


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
        staff_group, _ = Group.objects.get_or_create(name='staff')
        if _:
            logger.info(f'Создана новая группа безопасности: {staff_group}')
            staff_group.permissions.add(Permission.objects.get(name='Can view event'))
            staff_group.permissions.add(Permission.objects.get(name='Can change event'))
            staff_group.permissions.add(Permission.objects.get(name='Can delete event'))
            staff_group.permissions.add(Permission.objects.get(name='Can add event'))
            staff_group.permissions.add(Permission.objects.get(name='Can view task'))
            staff_group.permissions.add(Permission.objects.get(name='Can change task'))
            staff_group.permissions.add(Permission.objects.get(name='Can delete task'))
            staff_group.permissions.add(Permission.objects.get(name='Can add task'))
            staff_group.permissions.add(Permission.objects.get(name='Can view guest'))
            staff_group.permissions.add(Permission.objects.get(name='Can change guest'))
            staff_group.permissions.add(Permission.objects.get(name='Can delete guest'))
            staff_group.permissions.add(Permission.objects.get(name='Can add guest'))


        user_group, _ = Group.objects.get_or_create(name='user')
        if _:
            logger.info(f'Создана новая группа безопасности: {user_group}')
            user_group.permissions.add(Permission.objects.get(name='Can view event'))
            user_group.permissions.add(Permission.objects.get(name='Can view guest'))
            user_group.permissions.add(Permission.objects.get(name='Can add guest'))
            user_group.permissions.add(Permission.objects.get(name='Can change guest'))
            user_group.permissions.add(Permission.objects.get(name='Can delete guest'))

        site_domain = os.environ.get("SITE_DOMAIN", "localhost")
        site = Site.objects.first()
        if site.name == 'example.com':
            site.name = site_domain
            site.domain = site_domain
            site.save()
            logger.info(f'Добавлена настройка имени домена: {site_domain=}')
