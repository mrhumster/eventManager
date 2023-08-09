# Управление мероприятиями

## Установка

```bash
git clone https://github.com/mrhumster/eventManager.git
cd eventManager
docker-compose up -d
```

## .env файл

```env
POSTGRES_NAME=events
POSTGRES_USER=admin
POSTGRES_PASSWORD=password
POSTGRES_SERVICE=db
POSTGRES_PORT=5432
SECRET_KEY=DJANGO-SECRET
DEBUG=false
DJANGO_LOG_LEVEL=INFO
GUNICORN_LOG_LEVEL=info
RABBITMQ_DEFAULT_USER=admin
RABBITMQ_DEFAULT_PASS=admin
SMTP_HOST=smtp.domain.ru
SMTP_PORT=465
SMTP_USER=username@domain.ru
SMTP_PASSWORD=smtp-secret
DJANGO_SUPERUSER_PASSWORD=admin
DJANGO_SUPERUSER_EMAIL=user@domain.ru
DJANGO_SUPERUSER_USERNAME=admin
SITE_DOMAIN=domain.ru
```

## Точка для регистрации пришедших

```
METHODS: POST
URL: /api/guests/visit/
content-type: application/json
AUTH: basic
```

```json
{
  "event_id": 2,
  "first_name": "Антон",
  "last_name": "Хомяков",
  "image": "base64 image"
}
```
