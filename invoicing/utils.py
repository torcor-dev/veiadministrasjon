from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from .models import Faktura, FakturaLinje, Pris
from brukerliste.models import Bruker, Hytte

import weasyprint
import datetime
import decimal


def create_pdf(faktura):
    betalings_info = settings.SECRETS["FAKTURA"]
    ff_dato = faktura.faktura_dato + datetime.timedelta(days=betalings_info["FORFALL"])
    return render_to_string(
        "invoicing/pdf.html",
        {"faktura": faktura, "betalings_info": betalings_info, "forfall": ff_dato},
    )


def create_faktura(bruker, pris, beskjed=None):
    f = Faktura(bruker=bruker)
    if beskjed:
        f.beskjed = beskjed
    f.save()
    aar = f.faktura_dato
    prev_aar = aar - datetime.timedelta(days=365)
    periode = f"{prev_aar.year} / {aar.year}"
    for hytte in bruker.hytte.all()[:1]:
        p = pris.basis
        if hytte.sone == "Øvre":
            p += pris.ovre
        if p > 0:
            v_fl = FakturaLinje(
                faktura=f,
                hytte=hytte,
                tittel=f"Veiavgift {periode}",
                pris=decimal.Decimal(p),
            )
            v_fl.save()
        if bruker.broyting and pris.broyting > 0:
            b_fl = FakturaLinje(
                faktura=f,
                hytte=hytte,
                tittel=f"Brøyting {periode}",
                pris=decimal.Decimal(pris.broyting),
            )
            b_fl.save()
    if pris.annet:
        a_fl = FakturaLinje(
            faktura=f,
            hytte=None,
            tittel=pris.beskrivelse_annet,
            pris=decimal.Decimal(pris.annet),
        )
        a_fl.save()
    if f.get_total_sum() == 0:
        f.delete()
