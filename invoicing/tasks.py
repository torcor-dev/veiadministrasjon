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
    body = [
        f"Hei,\n",
        f"Her er faktura for foss-seterveien. \n\n",
        f"Faktura dato: {faktura.faktura_dato}\n",
        f"Forfallsdato: {faktura.faktura_dato + datetime.timedelta(days=betalings_info['FORFALL'])}\n",
        f"Bankkonto: {betalings_info['KONTONR']}\n\n",
        f"Å betale: {faktura.get_total_sum()}\n\n",
        f"Se vedlegg for detaljer.\n\n",
        f"Med vennlig hilsen \n",
        f"Foss-seterveien\n",
        f"v/ {betalings_info['NAVN']}\n",
        f"{betalings_info['GATE']}\n",
        f"{betalings_info['POSTSTED']}\n",
    ]

    email = EmailMessage(
        "Faktura - Foss-seterveien", "".join(body), to=["hjulenissen@gmail.com"]
    )  # [faktura.bruker.epost],)
    html = create_pdf(faktura)
    pdf = weasyprint.HTML(string=html).write_pdf()

    email.attach(f"Faktura_Foss-seterveien_{faktura.referanse}.pdf", pdf)
    email.send()
