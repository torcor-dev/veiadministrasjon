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


@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    url = "?{}={}".format(field_name, value)
    if urlencode:
        querystring = urlencode.split("&")
        filtered_querystring = filter(
            lambda p: p.split("=")[0] != field_name, querystring
        )
        encoded_querystring = "&".join(filtered_querystring)
        url = "{}&{}".format(url, encoded_querystring)
    return url
