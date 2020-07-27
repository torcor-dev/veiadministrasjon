from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
    TrigramSimilarity,
)
from django.db.models.functions import Greatest
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, reverse
from django.views.generic import DetailView, ListView

from .forms import (
    AdresseModelForm,
    BrukerModelForm,
    HytteModelForm,
    NyBrukerForm,
    PoststedModelForm,
    SearchForm,
    TelefonnrModelForm,
    RedigerBrukerForm,
)
from .models import Adresse, Bruker, Hytte, Poststed, Telefonnr


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
            # active
            "postnr": adresse.postnr.postnr,
            "poststed": adresse.postnr.poststed,
            "gate": adresse.gate,
            "tlf": tlf.nr,
        }

        bform = RedigerBrukerForm(initial=init, bruker=bruker)

    return render(request, "brukerliste/ny_bruker.html", {"bform": bform,},)


def bruker_search(request):
    form = SearchForm()
    query = None
    results = []
    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            if query == "":
                return HttpResponseRedirect(reverse("brukerliste"))
            # search_vector = SearchVector("etternavn", "fornavn")
            # search_query = SearchQuery(query)
            results = (
                Bruker.objects.annotate(
                    similarity=Greatest(
                        TrigramSimilarity("etternavn", query),
                        TrigramSimilarity("fornavn", query),
                        TrigramSimilarity("epost", query),
                    )
                )
                .filter(similarity__gt=0.4)
                .order_by("-similarity")
                #     search=search_vector, rank=SearchRank(search_vector, search_query)
                # )
                # .filter(search=search_query)
                # .order_by("-rank")
            )
        return render(
            request,
            "brukerliste/bruker_list.html",
            {"search_form": form, "query": query, "brukere": results},
        )
