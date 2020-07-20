from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Bruker


class BrukerSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Bruker.objects.all()

    def location(self, item):
        return reverse(item)

    def lastmod(self, obj):
        return obj.updated

