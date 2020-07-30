import django_filters
from django import forms
from .models import Faktura


class FakturaListeFilter(django_filters.FilterSet):
    sone = django_filters.ChoiceFilter(
        field_name="bruker__hytte__sone",
        choices=(("Nedre", "Nedre"), ("Øvre", "Øvre")),
        empty_label="Alle",
        distinct=True,
        label="Sone",
        widget=forms.RadioSelect,
    )
    broyting = django_filters.ChoiceFilter(
        field_name="bruker__broyting",
        distinct=True,
        empty_label="Alle",
        choices=((True, "Ja"), (False, "Nei")),
        label="Brøyting",
        widget=forms.RadioSelect,
    )
    betalt = django_filters.ChoiceFilter(
        field_name="betalt",
        empty_label="Alle",
        choices=((True, "Ja"), (False, "Nei")),
        distinct=True,
        label="Betalt",
        widget=forms.RadioSelect,
    )
    aar = django_filters.NumberFilter(
        field_name="faktura_dato", lookup_expr="year", label="År"
    )
    navn = django_filters.CharFilter(
        field_name="bruker__etternavn", lookup_expr="icontains", label="Etternavn"
    )
