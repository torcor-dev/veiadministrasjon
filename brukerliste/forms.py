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


class NyBrukerForm(forms.Form):
    SONER = [("Nedre", "Nedre"), ("Øvre", "Øvre")]
    HYTTER = [("Ny hytte", "Ny hytte"), ("Overdragelse", "Overdragelse")]

    fornavn = forms.CharField(max_length=100)
    etternavn = forms.CharField(max_length=100)
    epost = forms.EmailField()
    broyting = forms.BooleanField(required=False)
    faktureres = forms.BooleanField(required=False)

    postnr = forms.CharField(max_length=4)
    poststed = forms.CharField(max_length=100)
    gate = forms.CharField(max_length=150)

    tlf = forms.CharField(max_length=15)

    ny_hytte = forms.ChoiceField(
        choices=HYTTER, widget=forms.RadioSelect(), required=False
    )

    gnr = forms.CharField(max_length=4, required=False)
    bnr = forms.CharField(max_length=4, required=False)
    sone = forms.CharField(
        max_length=8, widget=forms.Select(choices=SONER), required=False
    )

    overdratt_fra = forms.ModelChoiceField(
        queryset=(Hytte.objects.all()), required=False
    )

    def clean(self):
        data = super().clean()

        epost = data.get("epost")
        tlf = data.get("tlf")
        gnr = data.get("gnr")
        bnr = data.get("bnr")
        if Bruker.objects.filter(epost=epost).exists():
            raise forms.ValidationError("Ikke unik epost adresse")
        elif Telefonnr.objects.filter(nr=tlf).exists():
            raise forms.ValidationError("Ikke unikt telefonnr")
        elif data.get("ny_hytte") == "Ny hytte" and (not gnr or not bnr):
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

        if data["ny_hytte"] == "Ny hytte":
            hytte = Hytte(
                eier=ny_bruker, gnr=data["gnr"], bnr=data["bnr"], sone=data["sone"]
            )
            hytte.save()
        elif data["ny_hytte"] == "Overdragelse":
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
    query = forms.CharField()
