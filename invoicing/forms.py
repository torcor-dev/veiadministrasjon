from django import forms
from django.contrib import messages
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
from .models import Faktura, Pris
from brukerliste.models import Bruker, Hytte


class PrisModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.csrf_token = False
        self.helper.layout = Layout(
            Row(
                Column("basis", css_class="form-group col-md-4 mb-0"),
                Column("ovre", css_class="form-group col-md-4 pt-6 mb-0"),
                Column("broyting", css_class="form-group col-md-4 mb-0"),
            ),
            Row(
                Column("annet", css_class="form-group col-md-4 mb-0"),
                Column("beskrivelse_annet", css_class="form-group col-md-8 mb-0"),
            ),
        )

    class Meta:
        model = Pris
        fields = "__all__"
        labels = {"ovre": "Øvre", "broyting": "Brøyting"}
        help_texts = {
            "basis": "Grunnpris/veiavgift for nedre sone, sett som 0 hvis det skal bare faktureres brøyting eller annet",
            "ovre": "Tillegg i veiavgift for øvre sone, legges automatisk til basisprisen",
            "annet": "Diverse annet, f.eks. purring, legges til som egen fakuralinje, husk beskrivelse",
        }

    def clean(self):
        data = super().clean()
        annet = data.get("annet")
        beskrivelse = data.get("beskrivelse_annet")
        if annet and not beskrivelse:
            raise forms.ValidationError("Mangler beskrivelse")
        if not annet and beskrivelse:
            raise forms.ValidationError("Mangler beløp")


class FakturaModelForm(forms.ModelForm):
    class Meta:
        model = Faktura
        fields = ["beskjed"]
        labels = {
            "besked": "Beskjed",
        }
        help_texts = {
            "beskjed": "Legg inn en eventuell beskjed til motakerene her",
        }
        widgets = {
            "beskjed": forms.Textarea(
                attrs={"rows": 1, "cols": 40, "style": "height: 5em;"}
            )
        }


class BrukerSelectForm(forms.Form):
    brukerliste = forms.ModelMultipleChoiceField(Bruker.objects.filter(active=True))


FILTER_HELPER = FormHelper()
FILTER_HELPER.form_method = "GET"
FILTER_HELPER.label_class = "text-muted"
FILTER_HELPER.layout = Layout(
    Row(
        Column("broyting", css_class="form-group col-md-4 mb-0"),
        Column("sone", css_class="form-group col-md-4 pt-6 mb-0"),
        Column("betalt", css_class="form-group col-md-4 mb-0"),
    ),
    Row(
        Column("navn", css_class="form-group col-md-8 mb-0"),
        Column("aar", css_class="form-group col-md-4 pt-6 mb-0 align-bottom"),
    ),
    Submit("search", "Søk", css_class="btn-secondary my-2 my-sm-0"),
)
