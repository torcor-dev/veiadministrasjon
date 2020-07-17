from django.contrib import admin

from .models import (Adresse, Bruker, Faktura, FakturaLinje, Hytte, Poststed,
                     Pris, Telefonnr, TidligereEier)

admin.site.register(Bruker)
admin.site.register(Hytte)
admin.site.register(Poststed)
admin.site.register(Faktura)
admin.site.register(FakturaLinje)
admin.site.register(Adresse)
admin.site.register(Telefonnr)
admin.site.register(Pris)
admin.site.register(TidligereEier)
