from django.urls import path
from . import views

urlpatterns = [
    path("<int:bruker_id>/", views.test_faktura, name="faktura"),
    path("<int:faktura_nr>/pdf/", views.faktura_pdf, name="faktura-pdf"),
]
