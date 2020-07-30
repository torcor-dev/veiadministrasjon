from django.urls import path
from . import views

urlpatterns = [
    path("<int:bruker_id>/", views.test_faktura, name="faktura"),
    path("<int:faktura_nr>/pdf/", views.faktura_pdf, name="faktura-pdf"),
    path("liste/<int:sone>/", views.faktura_liste, name="faktura-liste"),
    path("liste/", views.faktura_liste, name="faktura-liste"),
    path("send_mail/", views.send_mail, name="send-mail"),
]
