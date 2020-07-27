from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Fieldset,
    Submit,
    Div,
    MultiField,
    Button,
    Field,
    HTML,
    Column,
    Row,
)

from crispy_forms.bootstrap import FormActions, Accordion, AccordionGroup, InlineField
from datetime import datetime

from django import forms

from .models import (
    Adresse,
    Bruker,
    Hytte,
    Poststed,
    Telefonnr,
    TidligereEier,
)


class BrukerModelForm(forms.ModelForm):
    class Meta:
        model = Bruker
        fields = "__all__"


class AdresseModelForm(forms.ModelForm):
    class Meta:
        model = Adresse
        fields = ["gate"]


class PoststedModelForm(forms.ModelForm):
    class Meta:
        model = Poststed
        fields = "__all__"


class TelefonnrModelForm(forms.ModelForm):
    class Meta:
        model = Telefonnr
        fields = ["nr"]


class HytteModelForm(forms.ModelForm):
    class Meta:
        model = Hytte
        fields = ["gnr", "bnr", "sone"]


BRUKER_LAYOUT = Layout(
    Row(
        Column("fornavn", css_class="form-group col-md-6 mb-0"),
        Column("etternavn", css_class="form-group col-md-6 mb-0"),
    ),
    "gate",
    Row(
        Column("postnr", css_class="form-group col-md-4 mb-0"),
        Column("poststed", css_class="form-group col-md-8 mb-0"),
    ),
    "epost",
    Row(
        Column("tlf", css_class="form-group col-md-8 mb-0"),
        Column("broyting", css_class="form-group col-md-2 pt-5 mb-0"),
        Column("faktureres", css_class="form-group col-md-2 pt-5 mb-0"),
    ),
)


class BrukerForm(forms.Form):
    fornavn = forms.CharField(max_length=100)
    etternavn = forms.CharField(max_length=100)
    epost = forms.EmailField()
    broyting = forms.BooleanField(required=False, label="Brøyting")
    faktureres = forms.BooleanField(required=False)

    postnr = forms.CharField(max_length=4)
    poststed = forms.CharField(max_length=100)
    gate = forms.CharField(max_length=150, label="Gateadresse")

    tlf = forms.CharField(max_length=15, label="Telefon")


class RedigerBrukerForm(BrukerForm):
    def __init__(self, *args, **kwargs):
        self.bruker = kwargs.pop("bruker", None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            BRUKER_LAYOUT,
            FormActions(
                Submit("submit", "Lagre", css_class="button white"),
                Button("cancel", "Avbryt"),
            ),
        )

    def clean(self):
        data = super().clean()

        epost = data.get("epost")
        tlf = data.get("tlf")
        if Bruker.objects.filter(epost=epost).exclude(pk=self.bruker.pk).exists():
            raise forms.ValidationError("Ikke unik epost adresse")
        elif Telefonnr.objects.filter(nr=tlf).exclude(pk=self.bruker.pk).exists():
            raise forms.ValidationError("Ikke unikt telefonnr")

    def save(self):
        data = self.cleaned_data
        self.bruker.fornavn = data["fornavn"]
        self.bruker.etternavn = data["etternavn"]
        self.bruker.epost = data["epost"]
        self.bruker.broyting = data["broyting"]
        self.bruker.faktureres = data["faktureres"]
        self.bruker.save()

        psted = Poststed(postnr=data["postnr"], poststed=data["poststed"])
        try:
            psted.save()
        except:
            psted = Poststed.objects.get(postnr=data["postnr"])

        adr = self.bruker.adresse.first()
        adr.gate = data["gate"]
        adr.save()

        tlf = self.bruker.tlf.first()
        tlf.nr = data["tlf"]
        tlf.save()


class NyBrukerForm(BrukerForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            BRUKER_LAYOUT,
            Accordion(
                AccordionGroup(
                    "Ny hytte",
                    Row(
                        Column("gnr", css_class="form-group col-md-4 mb-0"),
                        Column("bnr", css_class="form-group col-md-4 mb-0"),
                        Column("sone", css_class="form-group col-md-4 mb-0"),
                    ),
                    css_id="ny_hytte",
                ),
                AccordionGroup("Overdragelse", "overdratt_fra", css_id="overdragelse",),
            ),
            Field("ny_hytte", value="None"),
            FormActions(
                Submit("submit", "Lagre", css_class="button white"),
                Button("cancel", "Avbryt"),
            ),
        )

    SONER = [("Nedre", "Nedre"), ("Øvre", "Øvre")]

    ny_hytte = forms.CharField(widget=forms.HiddenInput(), required=False)

    gnr = forms.CharField(max_length=4, required=False, label="GNR")
    bnr = forms.CharField(max_length=4, required=False, label="BNR")
    sone = forms.CharField(
        max_length=8, widget=forms.Select(choices=SONER), required=False
    )

    overdratt_fra = forms.ModelChoiceField(
        queryset=(Hytte.objects.all()), required=False
    )

    def clean(self):
        data = super().clean()

        gnr = data.get("gnr")
        bnr = data.get("bnr")
        epost = data.get("epost")
        tlf = data.get("tlf")
        if Bruker.objects.filter(epost=epost).exists():
            raise forms.ValidationError("Ikke unik epost adresse")
        elif Telefonnr.objects.filter(nr=tlf).exists():
            raise forms.ValidationError("Ikke unikt telefonnr")
        elif data.get("ny_hytte") == "ny_hytte":
            if not gnr or not bnr:
                raise forms.ValidationError("Manglende GNR eller BNR")
            elif Hytte.objects.filter(gnr=gnr, bnr=bnr).exists():
                raise forms.ValidationError("Hytten finnes fra før")
        else:
            return data

    def save(self):
        data = self.cleaned_data
        ny_bruker = Bruker(
            fornavn=data["fornavn"],
            etternavn=data["etternavn"],
            epost=data["epost"],
            broyting=data["broyting"],
            faktureres=data["faktureres"],
        )
        ny_bruker.save()

        psted = Poststed(postnr=data["postnr"], poststed=data["poststed"])
        try:
            psted.save()
        except:
            psted = Poststed.objects.get(postnr=data["postnr"])

        adr = Adresse(postnr=psted, bruker=ny_bruker, gate=data["gate"])
        adr.save()

        tlf = Telefonnr(bruker=ny_bruker, nr=data["tlf"])

        tlf.save()

        if data["ny_hytte"] == "ny_hytte":
            hytte = Hytte(
                eier=ny_bruker, gnr=data["gnr"], bnr=data["bnr"], sone=data["sone"]
            )
            hytte.save()
        elif data["ny_hytte"] == "overdragelse":
            g_hytte = Hytte.objects.get(pk=data["overdratt_fra"].pk)
            tidligere_eier = TidligereEier(
                hytte=g_hytte,
                gammel_eier=g_hytte.eier,
                ny_eier=ny_bruker,
                overdratt=datetime.now(),
            )
            g_hytte.eier = ny_bruker
            g_hytte.save()
            tidligere_eier.save()


class SearchForm(forms.Form):
    query = forms.CharField(required=False)
