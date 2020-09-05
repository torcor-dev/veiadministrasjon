from celery import task
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from .utils import create_pdf
from .models import Faktura
import weasyprint
import datetime


@task
def send_mail(faktura_pk):
    faktura = Faktura.objects.get(pk=faktura_pk)
    betalings_info = settings.SECRETS["FAKTURA"]
    beskjed = faktura.beskjed if faktura.beskjed else ""
    body = [
        f"Hei,\n",
        f"Her er faktura for Fossæterveien. \n\n",
        f"Faktura dato: {faktura.faktura_dato}\n",
        f"Forfallsdato: {faktura.faktura_dato + datetime.timedelta(days=betalings_info['FORFALL'])}\n",
        f"Bankkonto: {betalings_info['KONTONR']}\n\n",
        f"Å betale: {faktura.get_total_sum()}\n\n",
        f"Se vedlegg for detaljer.\n",
        beskjed,
        f"\nVi setter pris på at dere varsler om endringer av kontaktinformasjon, og at eventuell flytting og overdragelser, samt av- og påmelding for brøyting blir meldt til oss i godt tid.\n\n",
        f"Med vennlig hilsen \n",
        f"Fossæterveien\n",
        f"v/ {betalings_info['NAVN']}\n",
        f"{betalings_info['GATE']}\n",
        f"{betalings_info['POSTSTED']}\n",
    ]

    email = EmailMessage(
        "Faktura - Fossæterveien", "".join(body), to=["hjulenissen@gmail.com"]
    )  # [faktura.bruker.epost],)
    html = create_pdf(faktura)
    pdf = weasyprint.HTML(string=html).write_pdf()

    email.attach(f"Faktura_Fossæterveien_{faktura.referanse}.pdf", pdf)
    email.send()
