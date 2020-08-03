from django.urls import path
from . import views
from .views import FakturaDeleteView

urlpatterns = [
    path("<int:bruker_id>/", views.test_faktura, name="faktura"),
    path("<int:faktura_nr>/pdf/", views.faktura_pdf, name="faktura-pdf"),
    path("liste/", views.faktura_liste, name="faktura-liste"),
    path("utboks/slett/<int:pk>/", FakturaDeleteView.as_view(), name="faktura-slett"),
    path("utboks/slett/", views.slett_utboks, name="faktura-utboks-slett"),
    path("utboks/send/", views.send_utboks, name="faktura-utboks-send"),
    path("utboks/", views.utboks, name="faktura-utboks"),
    path("lag/", views.enkelt_faktura, name="faktura-lag"),
    path("lag_alle/", views.faktura_lag_alle, name="faktura-lag-alle"),
    path("send_mail/", views.send_mail, name="send-mail"),
    path("betalt/<int:pk>/", views.betalt_faktura, name="faktura-betalt"),
]
