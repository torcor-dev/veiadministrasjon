from django.db import models


class Poststed(models.Model):
    postnr = models.CharField(max_length=4, unique=True)
    poststed = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.postnr} {self.poststed}"


class Bruker(models.Model):
    fornavn = models.CharField(max_length=200)
    etternavn = models.CharField(max_length=200)
    epost = models.EmailField(max_length=250, unique=True)
    broyting = models.BooleanField()
    faktureres = models.BooleanField()
    notat = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.fornavn} {self.etternavn}"


class Adresse(models.Model):
    bruker = models.ForeignKey(Bruker, on_delete=models.CASCADE, related_name="adresse")
    postnr = models.ForeignKey(Poststed, on_delete=models.CASCADE)
    gate = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.bruker} {self.gate}"


class Telefonnr(models.Model):
    bruker = models.ForeignKey(Bruker, on_delete=models.CASCADE, related_name="tlf")
    nr = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return f"{self.bruker} {self.nr}"


class Hytte(models.Model):
    SONER = [("Nedre", "Nedre"), ("Øvre", "Øvre")]

    gnr = models.CharField(max_length=4)
    bnr = models.CharField(max_length=4)
    sone = models.CharField(max_length=8, choices=SONER)
    eier = models.ForeignKey(
        Bruker, on_delete=models.SET_NULL, null=True, related_name="hytte"
    )

    class Meta:
        unique_together = (
            "gnr",
            "bnr",
        )

    def __str__(self):
        return f"{self.gnr} {self.bnr} - {self.eier}"


class TidligereEier(models.Model):
    hytte = models.ForeignKey(Hytte, on_delete=models.CASCADE, related_name="tidligere_eier")
    gammel_eier = models.ForeignKey(Bruker, on_delete=models.CASCADE, related_name="gammel_eier")
    ny_eier = models.ForeignKey(Bruker, on_delete=models.CASCADE, related_name="ny_eier")
    overdratt = models.DateField()

    def __str__(self):
        return f"{self.hytte.gnr} {self.hytte.bnr} {self.gammel_eier} - {self.overdratt}"


class Pris(models.Model):
    basis_pris = models.IntegerField()
    vinter_pris = models.IntegerField()
    aar = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.aar}"


class Faktura(models.Model):
    bruker = models.ForeignKey(Bruker, on_delete=models.CASCADE)
    dato = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.bruker} {self.dato}"


class FakturaLinje(models.Model):
    pris = models.ForeignKey(Pris, on_delete=models.CASCADE)
    hytte = models.ForeignKey(Hytte, on_delete=models.CASCADE)
    faktura = models.ForeignKey(Faktura, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.faktura} {self.hytte}"
