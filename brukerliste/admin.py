from django.contrib import admin

from .models import (
    Adresse,
    Bruker,
    Hytte,
    Poststed,
    Telefonnr,
    TidligereEier,
)

admin.site.register(Hytte)
admin.site.register(Poststed)
admin.site.register(Adresse)
admin.site.register(Telefonnr)
admin.site.register(TidligereEier)


@admin.register(Bruker)
class BrukerAdmin(admin.ModelAdmin):
    list_display = ("etternavn", "fornavn", "epost", "broyting", "faktureres")
    list_filter = ("faktureres", "broyting")
    search_fields = ("etternavn",)

    # other neat fields:
    # raw_id_fields = ('foreign key')
    # ordering = ('etternavn', 'fornavn')

