from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf.urls.static import static

# from django.contrib.sitemaps.views import sitemap
# from brukerliste.sitemaps import BrukerSitemap

# sitemaps = {
#     "brukere": BrukerSitemap,
# }

urlpatterns = [
    path("admin/", admin.site.urls),
    path("faktura/", include("invoicing.urls")),
    path("account/", include("account.urls")),
    path("", include("brukerliste.urls")),
    # path(
    #     "sitemap.xml",
    #     sitemap,
    #     {"sitemaps": sitemaps},
    #     name="django.contrib.sitemaps.views.sitemap",
    # ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
