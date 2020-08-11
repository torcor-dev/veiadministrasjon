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
    betalings_info = settings.SECRETS["FAKTURA"]
    body = f"""
               Hei,\n
               Her er faktura for foss-seterveien. \n\n
               Faktura dato: {faktura.faktura_dato}\n
               Forfallsdato: {faktura.faktura_dato + datetime.timedelta(days=betalings_info["FORFALL"])}\n
               Bankkonto: {betalings_info["KONTONR"]}\n\n
               Å betale: {faktura.get_total_sum()}\n\n
               Se vedlegg for detaljer.\n\n
               Med vennlig hilsen \n
               Foss-seterveien\n
               v/ {betalings_info['NAVN']}\n
               {betalings_info['GATE']}\n
               {betalings_info['POSTSTED']}\n

            """
    email = EmailMessage(
        "Faktura - Foss-seterveien",
        body,
        "hjulenissen@gmail.com",
        [faktura.bruker.epost],
    )
    html = create_pdf(faktura)
    pdf = weasyprint.HTML(string=html).write_pdf()

    email.attach(f"Faktura_Foss-seterveien_{faktura.referanse}_pdf", pdf)
    email.send()


def create_faktura(bruker, pris):
    f = Faktura(bruker=bruker)
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
