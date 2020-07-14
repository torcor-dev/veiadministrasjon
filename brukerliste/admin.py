from django.contrib import admin
from .models import (
        Bruker, Hytte, Poststed, Faktura, FakturaLinje, Adresse, 
        Telefonnr, Tester, Pris, 
        )

admin.site.register(Bruker)
admin.site.register(Hytte)
admin.site.register(Poststed)
admin.site.register(Faktura)
admin.site.register(FakturaLinje)
admin.site.register(Adresse)
admin.site.register(Telefonnr)
admin.site.register(Tester)
admin.site.register(Pris)
