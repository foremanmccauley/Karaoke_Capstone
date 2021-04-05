import requests
from django import template

register = template.Library()

@register.simple_tag
def upload_file(request):
    return('Successfully uploaded file')