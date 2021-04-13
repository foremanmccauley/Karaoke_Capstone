import requests
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def upload_file(request, f):
    ret = '<audio src=' + f
    ret += '> Your browser does not support the <code>audio</code> element.</audio>'
    return mark_safe(ret)