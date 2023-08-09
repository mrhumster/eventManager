# Управление мероприятиями

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
