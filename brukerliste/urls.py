from django.urls import path

from .views import (
    ny_bruker,
    rediger_bruker,
    hytte_update,
    OverdragelseListView,
    bruker_list_view,
    ny_hytte,
    eksporter_brukerliste_csv,
)

urlpatterns = [
    path("", bruker_list_view, name="brukerliste"),
    path("ny_bruker/", ny_bruker, name="ny-bruker"),
    path("rediger_bruker/<int:pk>", rediger_bruker, name="rediger-bruker"),
    path("ny_hytte/<int:pk>/", ny_hytte, name="ny-hytte"),
    path("hytter/<int:pk>/", hytte_update, name="hytte-update"),
    path("overdragelser/", OverdragelseListView.as_view(), name="overdragelser"),
    path("eksporter/", eksporter_brukerliste_csv, name="eksporter-brukerliste-csv"),
]
