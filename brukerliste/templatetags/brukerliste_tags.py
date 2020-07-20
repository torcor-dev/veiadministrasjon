from django import template
from ..models import Bruker, TidligereEier

register = template.Library()


@register.simple_tag
def total_brukere():
    return Bruker.objects.all().count()


@register.inclusion_tag("brukerliste/siste_overdragelser.html")
def show_last_transfers(count=5):
    last_transfers = TidligereEier.objects.all().order_by("-overdratt")[:count]
    return {"last_transfers": last_transfers}


"""
# custom markdown filter

from django.utils.safestring import mark_safe
import markdown

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

# usage: {{ variable | markdown }}
"""
