from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse
from django.template.loader import render_to_string
from django.views.generic import DeleteView
from .models import Faktura, FakturaLinje, Pris
from .utils import create_pdf, create_faktura, send_mail
from .filters import FakturaListeFilter
from .forms import PrisModelForm, BrukerSelectForm, FILTER_HELPER
from brukerliste.models import Bruker, Hytte
from django.contrib.auth.decorators import user_passes_test

import weasyprint
import datetime
import decimal
import csv


def eksporter_fakturaoversikt_csv(request):
    response = HttpResponse(content_type="text/csv")
    dato = datetime.datetime.today().strftime("%d-%m-%Y")
    response[
        "Content-Disposition"
    ] = f"attachment; filename=fsv_fakturaoversikt_{dato}.csv"

    writer = csv.writer(response)
    faktura = Faktura.objects.all().order_by("-faktura_dato", "-oppdatert_dato")
    writer.writerow(
        ["Dato", "Navn", "Hytter", "Brøyting", "Total beløp", "Betalt",]
    )

    for f in faktura:
        hytter = [f"{h.gnr} - {h.bnr}" for h in f.bruker.hytte.all()]
        writer.writerow(
            [
                str(f.faktura_dato.strftime("%d/%m/%Y")),
                str(f.bruker),
                str(" ".join(hytter)),
                str(f.bruker.broyting),
                str(f.get_total_sum()),
                str(f.betalt),
            ]
        )
    return response


def faktura_pdf(request, faktura_nr):
    faktura = get_object_or_404(Faktura, id=faktura_nr)
    html = create_pdf(faktura)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"filename=faktura_{faktura.referanse}.pdf"
    weasyprint.HTML(string=html).write_pdf(response)
    return response


def faktura_liste(request):
    fl = FakturaListeFilter(
        request.GET,
        queryset=Faktura.objects.filter(sendt=True).order_by(
            "-faktura_dato", "-oppdatert_dato"
        ),
    )
    paginator = Paginator(fl.qs, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "invoicing/faktura_list.html",
        {"filter": fl, "page_obj": page_obj, "FILTER_HELPER": FILTER_HELPER},
    )


# def perm_check(user):
#    return user.has_perm("invoicing.add_faktura")


# @user_passes_test(perm_check, login_url="../", redirect_field_name=None)
def enkelt_faktura(request):
    if request.method == "POST":
        pris_form = PrisModelForm(request.POST)
        bruker_form = BrukerSelectForm(request.POST)
        if pris_form.is_valid() and bruker_form.is_valid():
            p = pris_form.save()
            bcd = bruker_form.cleaned_data
            for b in bcd["brukerliste"]:
                create_faktura(b, p)
            messages.success(request, "Fakturaen(e) er lagt til i utboksen")
            return HttpResponseRedirect(reverse("faktura-utboks"))
        messages.error(request, "Fakturaen(e) ble ikke lagt til i utboksen")
    pris_form = PrisModelForm(instance=Pris.objects.last())
    bruker_form = BrukerSelectForm()
    return render(
        request,
        "invoicing/enkelt_faktura.html",
        {"pris_form": pris_form, "bruker_form": bruker_form},
    )


def faktura_lag_alle(request):
    if request.method == "POST":
        pris_form = PrisModelForm(request.POST)
        if pris_form.is_valid():
            p = pris_form.save()
            bl = Bruker.objects.filter(
                hytte__isnull=False, faktureres=True, active=True
            ).distinct()
            for b in bl:
                create_faktura(b, p)
            messages.success(request, "Fakturaen(e) er lagt til i utboksen")
            return HttpResponseRedirect(reverse("faktura-utboks"))
        messages.error(request, "Fakturaen(e) ble ikke lagt til i utboksen")
    pris_form = PrisModelForm(instance=Pris.objects.last())
    return render(request, "invoicing/faktura_lag_alle.html", {"pris_form": pris_form},)


def purring(request):
    dato = datetime.datetime.now() - datetime.timedelta(
        days=settings.SECRETS["FAKTURA"]["FORFALL"]
    )
    fakturaer = Faktura.objects.filter(sendt=True, betalt=False, faktura_dato__lt=dato)
    if fakturaer:
        for f in fakturaer:
            f.faktura_dato = datetime.date.today()
            f.sendt = False
            f.save()
        messages.info(request, "Fakturaen(e) er lagt til i utboksen")
        return HttpResponseRedirect(reverse("faktura-utboks"))
    return HttpResponseRedirect(reverse("faktura-liste"))


def utboks(request):
    fakturaer = Faktura.objects.filter(sendt=False).order_by("-timestamp")
    return render(request, "invoicing/faktura_utboks.html", {"fakturaer": fakturaer})


def send_utboks(request):
    ctx = "Send"
    if request.method == "POST":
        fakturaer = Faktura.objects.filter(sendt=False)
        for f in fakturaer:
            if f.bruker.epost:
                send_mail(f)
                f.sendt = True
                f.save()
        return HttpResponseRedirect(reverse("faktura-utboks"))
    return render(request, "invoicing/faktura_utboks_confirm.html", {"ctx": ctx})


def send_utboks_post(request):
    markering = "Marker alle fakturaer uten epost adresse som sendt"
    if request.method == "POST":
        fakturaer = Faktura.objects.filter(sendt=False, bruker__epost="")
        for f in fakturaer:
            f.sendt = True
            f.save()
        return HttpResponseRedirect(reverse("faktura-utboks"))
    return render(
        request, "invoicing/faktura_utboks_confirm.html", {"markering": markering}
    )


def slett_utboks(request):
    ctx = "Slett"
    if request.method == "POST":
        fakturaer = Faktura.objects.filter(sendt=False)
        fakturaer.delete()
        return HttpResponseRedirect(reverse("faktura-utboks"))
    return render(request, "invoicing/faktura_utboks_confirm.html", {"ctx": ctx})


class FakturaDeleteView(DeleteView):
    model = Faktura
    success_url = "/faktura/utboks/"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def test_func(self):
        faktura = self.get_object()
        if not faktura.sendt:
            return True
        return False


def betalt_faktura(request, pk):
    faktura = get_object_or_404(Faktura, pk=pk)
    if faktura.betalt:
        faktura.betalt = False
        faktura.save()
    else:
        faktura.betalt = True
        faktura.save()
    # redirect to previous url, which contains filter settings.
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
