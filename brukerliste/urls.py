from django.urls import path

from .views import (
    BrukerDetailView,
    BrukerListView,
    HytteListView,
    NyBruker,
    bruker_search,
    rediger_bruker,
    hytte_update,
    OverdragelseListView,
)

urlpatterns = [
    path("", BrukerListView.as_view(), name="brukerliste"),
    path("bruker/<int:pk>/", BrukerDetailView.as_view(), name="bruker-detail"),
    path("hytter/", HytteListView.as_view(), name="hytteliste"),
    path("ny_bruker/", NyBruker, name="ny-bruker"),
    path("rediger_bruker/<int:pk>", rediger_bruker, name="rediger-bruker"),
    path("bruker_sok/", bruker_search, name="bruker-search"),
    path("hytter/<int:pk>/", hytte_update, name="hytte-update"),
    path("overdragelser/", OverdragelseListView.as_view(), name="overdragelser"),
]
