from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .forms import (
    NyBrukerForm,
    BrukerModelForm,
    AdresseModelForm,
    PoststedModelForm,
    TelefonnrModelForm,
    HytteModelForm,
)
from .models import Bruker, Faktura, Hytte, Poststed, Adresse, Telefonnr


class HytteListView(ListView):
    model = Hytte
    context_object_name = "hytter"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx


class BrukerListView(ListView):
    model = Bruker
    context_object_name = "brukere"
    ordering = ["etternavn"]


class BrukerDetailView(DetailView):
    model = Bruker


def NyBruker(request):
    if request.method == "POST":
        bform = NyBrukerForm(request.POST)
        if bform.is_valid():
            bform.save()
            return HttpResponseRedirect("../")
    else:
        bform = NyBrukerForm()

    return render(request, "brukerliste/ny_bruker.html", {"bform": bform,},)


def RedigerBruker(request, pk):
    bruker = get_object_or_404(Bruker, pk=pk)
    adresse = get_object_or_404(Adresse, bruker=bruker)
    tlf = get_object_or_404(Telefonnr, bruker=bruker)
    # hytte = get_object_or_404(Hytte, eier=bruker)
    if request.method == "POST":
        bform = BrukerModelForm(request.POST, instance=bruker)
        aform = AdresseModelForm(request.POST, instance=adresse)
        pform = PoststedModelForm(request.POST, instance=adresse.postnr)
        tform = TelefonnrModelForm(request.POST, instance=tlf)
        # hform = HytteModelForm(request.POST, instance=hytte)
        if (
            bform.is_valid()
            and aform.is_valid()
            and pform.is_valid()
            and tform.is_valid()
            # and hform.is_valid()
        ):
            bform.save()
            aform.save()
            pform.save()
            tform.save()
            # hform.save()
            return HttpResponseRedirect("../")
    else:
        bform = BrukerModelForm(instance=bruker)
        aform = AdresseModelForm(instance=adresse)
        pform = PoststedModelForm(instance=adresse.postnr)
        tform = TelefonnrModelForm(instance=tlf)
        # hform = HytteModelForm(instance=hytte)

    return render(
        request,
        "brukerliste/rediger_bruker.html",
        {
            "bform": bform,
            "aform": aform,
            "pform": pform,
            "tform": tform,
            # "hform": hform,
        },
    )
