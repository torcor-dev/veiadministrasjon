from django.db import models
from brukerliste.models import Bruker, Hytte

import decimal
import uuid


class Faktura(models.Model):
    referanse = models.UUIDField(default=uuid.uuid4, editable=False)
    bruker = models.ForeignKey(Bruker, on_delete=models.CASCADE, related_name="faktura")
    timestamp = models.DateTimeField(auto_now_add=True)
    faktura_dato = models.DateField(auto_now_add=True)
    oppdatert_dato = models.DateTimeField(auto_now=True)
    betalt = models.BooleanField(default=False)
    sendt = models.BooleanField(default=False)
    beskjed = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Fakturanr {self.id} - {self.faktura_dato} {self.bruker}"

    def get_total_sum(self):
        return sum(fl.pris for fl in self.fakturalinje.all())


class FakturaLinje(models.Model):
    faktura = models.ForeignKey(
        Faktura, on_delete=models.CASCADE, related_name="fakturalinje"
    )
    hytte = models.ForeignKey(
        Hytte, on_delete=models.CASCADE, related_name="flinje", null=True
    )
    tittel = models.CharField(max_length=250)
    pris = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Fakturalinje {self.id}"


class Pris(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    basis = models.DecimalField(max_digits=10, decimal_places=2)
    ovre = models.DecimalField(max_digits=10, decimal_places=2)
    broyting = models.DecimalField(max_digits=10, decimal_places=2)
    beskrivelse_annet = models.CharField(max_length=250, blank=True, null=True)
    annet = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=decimal.Decimal(0),
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"Priser {self.timestamp}"
