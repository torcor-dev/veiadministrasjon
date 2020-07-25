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
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

from .forms import (
    AdresseModelForm,
    BrukerModelForm,
    HytteModelForm,
    NyBrukerForm,
    PoststedModelForm,
    SearchForm,
    TelefonnrModelForm,
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
            messages.success(request, "Endringene er lagret")
            return HttpResponseRedirect("../")
        else:
            messages.error(request, "Endringene kunne ikke gjennomføres")

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


def bruker_search(request):
    form = SearchForm()
    query = None
    results = []

    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            # search_vector = SearchVector("etternavn", "fornavn")
            # search_query = SearchQuery(query)
            results = (
                Bruker.objects.annotate(
                    similarity=Greatest(
                        TrigramSimilarity("etternavn", query),
                        TrigramSimilarity("fornavn", query),
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
