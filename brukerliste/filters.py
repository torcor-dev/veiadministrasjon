import django_filters
from django import forms
from .models import Bruker


class BrukerListeFilter(django_filters.FilterSet):
    navn = django_filters.CharFilter(
        field_name="etternavn", lookup_expr="icontains", label="Etternavn"
    )
    gnr = django_filters.NumberFilter(
        field_name="hytte__gnr", label="GNR", distinct=True,
    )
    bnr = django_filters.NumberFilter(
        field_name="hytte__bnr", label="BNR", distinct=True,
    )
    sone = django_filters.ChoiceFilter(
        field_name="hytte__sone",
        choices=(("Nedre", "Nedre"), ("Øvre", "Øvre")),
        empty_label="Alle",
        distinct=True,
        label="Sone",
        widget=forms.RadioSelect,
    )
    broyting = django_filters.ChoiceFilter(
        field_name="broyting",
        distinct=True,
        empty_label="Alle",
        choices=((True, "Ja"), (False, "Nei")),
        label="Brøyting",
        widget=forms.RadioSelect,
    )
