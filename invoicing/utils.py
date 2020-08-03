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


def send_mail(faktura):
    email = EmailMessage(
        "test mail 1", "body message", "hjulenissen@gmail.com", [faktura.bruker.epost],
    )
    html = create_pdf(faktura)
    pdf = weasyprint.HTML(string=html).write_pdf()

    email.attach(f"Faktura.{faktura.id}.pdf", pdf)
    email.send()


def create_faktura(bruker, pris):
    f = Faktura(bruker=bruker)
    f.save()
    for hytte in bruker.hytte.all():
        p = pris.basis
        if hytte.sone == "Øvre":
            p += pris.ovre
        v_fl = FakturaLinje(
            faktura=f, hytte=hytte, tittel="Veiavgift", pris=decimal.Decimal(p)
        )
        v_fl.save()
        if bruker.broyting:
            b_fl = FakturaLinje(
                faktura=f,
                hytte=hytte,
                tittel="Brøyting",
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
    return f
