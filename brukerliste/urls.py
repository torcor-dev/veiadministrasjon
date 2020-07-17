from django.urls import path

from .views import BrukerDetailView, BrukerListView, HytteListView, NyBruker

urlpatterns = [
    path("", BrukerListView.as_view(), name="brukerliste"),
    path("bruker/<int:pk>/", BrukerDetailView.as_view(), name="bruker-detail"),
    path("hytter/", HytteListView.as_view(), name="hytteliste"),
    path("ny_bruker/", NyBruker, name="ny-bruker"),
]
