from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from .models import Faktura, FakturaLinje, Pris
from .utils import create_pdf, create_faktura, send_mail
from .filters import FakturaListeFilter
from brukerliste.models import Bruker, Hytte

import weasyprint
import datetime
import decimal


def test_faktura(request, bruker_id):
    bruker = get_object_or_404(Bruker, pk=bruker_id)
    pris = Pris.objects.first()
    faktura = create_faktura(bruker, pris)

    return render(request, "invoicing/faktura.html", {"faktura": faktura})


def faktura_pdf(request, faktura_nr):
    faktura = get_object_or_404(Faktura, id=faktura_nr)
    html = create_pdf(faktura)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"filename=faktura_{faktura.referanse}.pdf"
    weasyprint.HTML(string=html).write_pdf(response)
    return response


def faktura_liste(request, sone=None):
    fl = FakturaListeFilter(
        request.GET, queryset=Faktura.objects.all().order_by("-faktura_dato")
    )
    return render(request, "invoicing/faktura_list.html", {"filter": fl})
