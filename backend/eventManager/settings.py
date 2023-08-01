"""
Django settings for eventManager project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-1k$jlyn5qu7b8%gq^&9hvouiyw(a+8-0(onubjv=jdd^)$-2ue')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'NO').lower() in ('on', 'true', 'y', 'yes')

ALLOWED_HOSTS = ['localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.sites',
    'django_celery_results',
    'django_celery_beat',
    'bootstrap5',
    'accounts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'eventManager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'eventManager.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_NAME', 'base'),
        'USER': os.environ.get('POSTGRES_USER', 'admin'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', '12qwasZX'),
        'HOST': os.environ.get('POSTGRES_SERVICE', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', 5432),
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Asia/Omsk'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = '/static'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'


STORAGE = './media'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/'
LOGOUT_URL = '/accounts/logout/'

# CELERY
CELERY_BROKER_URL = f'pyamqp://{os.environ.get("RABBITMQ_DEFAULT_USER", "admin")}:{os.environ.get("RABBITMQ_DEFAULT_PASSWORD", "admin")}@rabbit:5672/'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
# EMAIL
EMAIL_HOST = os.environ.get('SMTP_HOST')
EMAIL_PORT = os.environ.get('SMTP_PORT')
EMAIL_HOST_USER = os.environ.get('SMTP_USER', 'test@email.yes')
EMAIL_HOST_PASSWORD = os.environ.get('SMTP_PASSWORD')
EMAIL_USE_SSL = True  # TLS settings

SITE_ID = 1

SITE_SCHEMA = 'https'    # http/https?

MODERATOR_MAIL = os.getenv('DJANGO_SUPERUSER_EMAIL', 'mr.humster@gmail.com')

AUTHENTICATION_BACKENDS = ['accounts.backends.CaseInsensitiveModelBackend']

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        'verbose': {
            'format': '{asctime} {levelname} {module} {message} {process:d} {thread:d}',
            'style': '{',
            'datefmt': "%d/%m/%Y %H:%M:%S"
        },
        'simple': {
            'format': '{asctime} {levelname} {message}',
            'style': '{',
            'datefmt': "%d/%m/%Y %H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "level": os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'class': 'logging.handlers.RotatingFileHandler',
            "filename": '/var/log/django/django.log',
            "formatter": "verbose",
            'maxBytes': 1024 * 1024 * 5,
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
    },
    "loggers": {
        "django": {
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            "handlers": ["console", "file"],
            "propagate": True,
        }
    },
}

SITE_ID = 1

SITE_SCHEMA = 'https'    # http/https?

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CSRF_TRUSTED_ORIGINS = ['https://base', 'https://base.vniigaz.local', 'https://192.168.1.100', 'https://localhost']