from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from .models import Faktura, FakturaLinje, Pris
from brukerliste.models import Bruker, Hytte

import weasyprint
import datetime
import decimal


def lag_faktura(bruker, pris, annet=None):
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
        if annet:
            a_fl = FakturaLinje(
                faktura=f, hytte=hytte, tittel=annet, pris=decimal.Decimal(pris.annet)
            )
            a_fl.save()
    return f


def test_faktura(request, bruker_id):
    bruker = get_object_or_404(Bruker, pk=bruker_id)
    pris = Pris.objects.first()
    faktura = lag_faktura(bruker, pris)

    return render(request, "invoicing/faktura.html", {"faktura": faktura})


def faktura_pdf(request, faktura_nr):
    betalings_info = settings.SECRETS["FAKTURA"]
    faktura = get_object_or_404(Faktura, id=faktura_nr)
    ff_dato = faktura.faktura_dato + datetime.timedelta(days=betalings_info["FORFALL"])
    html = render_to_string(
        "invoicing/pdf.html",
        {"faktura": faktura, "betalings_info": betalings_info, "forfall": ff_dato},
    )
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"filename=faktura_{faktura.referanse}.pdf"
    weasyprint.HTML(string=html).write_pdf(response)
    return response


# Create your views here.
