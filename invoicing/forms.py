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


class BrukerSelectForm(forms.Form):
    brukerliste = forms.ModelMultipleChoiceField(
        Bruker.objects.filter(faktureres=True, active=True)
    )


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
