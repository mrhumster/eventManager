import json
import math

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter()
@stringfilter
def padding(value):
    return int(value)*20


@register.filter()
@stringfilter
def deasterix(value):
    return value.replace("*", "8")



@register.filter()
@stringfilter
def humanize(size_bytes):
    size_bytes = int(size_bytes)
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


@register.filter
def guest_icon(value):
    match value:
        case 'REGISTERED':
            return '<i class="bi bi-person-fill text-primary pe-2" data-bs-toggle="tooltip" data-bs-placement="bottom" data-bs-title="Пользователь зарегистрирован"></i>'
        case 'REFUSED':
            return f'<i class="bi bi-person-fill-slash text-secondary pe-2" data-bs-toggle="tooltip" data-bs-placement="bottom" data-bs-title="Регистрация отменена"></i>'
        case 'VISITED':
            return f'<i class="bi bi-person-fill-check text-success pe-2" data-bs-toggle="tooltip" data-bs-placement="bottom" data-bs-title="Посетил мероприятие"></i>'

    return value
