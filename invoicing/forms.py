from django import forms
from django.contrib import messages
from .models import Faktura, Pris
from brukerliste.models import Bruker, Hytte


class PrisModelForm(forms.ModelForm):
    class Meta:
        model = Pris
        fields = "__all__"

    def clean(self):
        data = super().clean()
        annet = data.get("annet")
        beskrivelse = data.get("beskrivelse_annet")
        if annet and not beskrivelse:
            raise forms.ValidationError("Mangler beskrivelse")
        if not annet and beskrivelse:
            raise forms.ValidationError("Mangler beløp")


class BrukerSelectForm(forms.Form):
    brukerliste = forms.ModelMultipleChoiceField(Bruker.objects.filter(faktureres=True))

