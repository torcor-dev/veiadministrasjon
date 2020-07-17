from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .forms import NyBrukerForm
from .models import Bruker, Faktura, Hytte, Poststed


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
    # TODO Valg mellom ny hytte eller overtakelse av annen hytte
    if request.method == "POST":
        bform = NyBrukerForm(request.POST)
        if bform.is_valid():
            bform.save()
            return HttpResponseRedirect("../")
    else:
        bform = NyBrukerForm()

    return render(request, "brukerliste/ny_bruker.html", {"bform": bform,},)
