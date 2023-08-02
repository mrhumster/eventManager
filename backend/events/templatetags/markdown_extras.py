from django import template
from django.template.defaultfilters import stringfilter

import markdown as md

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=[
        'markdown.extensions.tables',
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.attr_list',
        'markdown.extensions.def_list',
        'markdown.extensions.sane_lists'
    ])
