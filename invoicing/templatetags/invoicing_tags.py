from django import template
from ..models import Faktura

register = template.Library()


@register.simple_tag
def usendte_fakturaer():
    fs = Faktura.objects.filter(sendt=False).count()
    if fs > 0:
        return fs
    else:
        return 0
