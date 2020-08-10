from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, reverse
from django.views.generic import ListView
from datetime import datetime

from .forms import (
    HytteModelForm,
    NyBrukerForm,
    RedigerBrukerForm,
    NyHytteForm,
    FILTER_HELPER,
)
from .models import Adresse, Bruker, Hytte, Poststed, Telefonnr, TidligereEier
from .filters import BrukerListeFilter

import csv


def eksporter_brukerliste_csv(request):
    response = HttpResponse(content_type="text/csv")
    dato = datetime.today().strftime("%d-%m-%Y")
    response["Content-Disposition"] = f"attachment; filename=fsv_brukerliste_{dato}.csv"

    writer = csv.writer(response)
    brukere = Bruker.objects.filter(active=True).order_by("etternavn")
    writer.writerow(
        [
            "Etternavn",
            "Fornavn",
            "Hytter",
            "Gateadresse",
            "Postnr",
            "Poststed",
            "Telefon",
            "Epost",
            "Brøyting",
            "Faktureres",
            "Notat",
        ]
    )

    for b in brukere:
        hytter = [f"{h.gnr} - {h.bnr}" for h in b.hytte.all()]
        writer.writerow(
            [
                str(b.etternavn),
                str(b.fornavn),
                str(" ".join(hytter)),
                str(b.adresse.first().gate),
                str(b.adresse.first().postnr.postnr),
                str(b.adresse.first().postnr.poststed),
                str(b.tlf.first().nr),
                str(b.epost),
                str(b.broyting),
                str(b.faktureres),
                str(b.notat),
            ]
        )
    return response


def bruker_list_view(request):
    fl = BrukerListeFilter(
        request.GET, queryset=Bruker.objects.filter(active=True).order_by("etternavn"),
    )
    brukere = fl.qs
    return render(
        request,
        "brukerliste/bruker_list.html",
        {"filter": fl, "brukere": brukere, "FILTER_HELPER": FILTER_HELPER},
    )


def ny_bruker(request):
    if request.method == "POST":
        bform = NyBrukerForm(request.POST)
        if bform.is_valid():
            bform.save()
            messages.success(request, "En ny bruker ble lagt til")
            return HttpResponseRedirect("../")
        else:
            messages.error(request, "Kunne ikke legge til brukeren")
    else:
        bform = NyBrukerForm()

    return render(request, "brukerliste/ny_bruker.html", {"bform": bform,},)


def rediger_bruker(request, pk):
    bruker = get_object_or_404(Bruker, pk=pk)
    adresse = bruker.adresse.first()  # get_object_or_404(Adresse, bruker=bruker)
    tlf = bruker.tlf.first()  # get_object_or_404(Telefonnr, bruker=bruker)
    fakturaer = bruker.faktura.all().order_by("-faktura_dato")[:5]
    if request.method == "POST":
        bform = RedigerBrukerForm(request.POST, bruker=bruker)
        if bform.is_valid():
            bform.save()
            messages.success(request, "Endringene er lagret")
            return HttpResponseRedirect("../")
        else:
            messages.error(request, "Kunne gjennomføre endringene")
    else:
        init = {
            "fornavn": bruker.fornavn,
            "etternavn": bruker.etternavn,
            "epost": bruker.epost,
            "broyting": bruker.broyting,
            "faktureres": bruker.faktureres,
            "postnr": adresse.postnr.postnr,
            "poststed": adresse.postnr.poststed,
            "gate": adresse.gate,
            "tlf": tlf.nr,
            "notat": bruker.notat,
            "aktiv": bruker.active,
        }

        bform = RedigerBrukerForm(initial=init, bruker=bruker)

    return render(
        request,
        "brukerliste/rediger_bruker.html",
        {"bform": bform, "bruker": bruker, "fakturaer": fakturaer},
    )


def ny_hytte(request, pk):
    bruker = get_object_or_404(Bruker, pk=pk)
    if request.method == "POST":
        form = NyHytteForm(request.POST, bruker=bruker)
        if form.is_valid():
            form.save()
            messages.success(request, "Endringere er lagret")
            return HttpResponseRedirect(reverse("rediger-bruker", args=[pk]))
        else:
            messages.error(request, "Kunne gjennomføre endringene")
    else:
        form = NyHytteForm(bruker=bruker)
        return render(
            request, "brukerliste/ny_hytte.html", {"form": form, "bruker": bruker}
        )
    pass


def hytte_update(request, pk):
    hytte = get_object_or_404(Hytte, pk=pk)
    cur_eier = hytte.eier
    if request.method == "POST":
        form = HytteModelForm(request.POST, instance=hytte)
        if form.is_valid():
            cd = form.cleaned_data
            if cd["eier"] != cur_eier:
                overdragelse = TidligereEier(
                    ny_eier=cd["eier"],
                    gammel_eier=cur_eier,
                    hytte=hytte,
                    overdratt=datetime.today(),
                )
                overdragelse.save()
                messages.success(request, "En ny overdragelse er registrert")
            form.save()
            messages.success(request, "Endringene er lagret")
        else:
            messages.error(
                request,
                "Endringene kunne ikke gjennomføres, sjekk at alle feltene er rikgtig utfylt",
            )
        return HttpResponseRedirect(reverse("hytte-update", args=[pk]))
    form = HytteModelForm(instance=hytte)
    return render(request, "brukerliste/hytte_update_form.html", {"form": form})


class OverdragelseListView(ListView):
    model = TidligereEier
    context_object_name = "overdragelser"
    template_name = "brukerliste/overdragelse_list.html"
    ordering = ["-overdratt"]
