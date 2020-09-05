from django.contrib import admin
from .models import Faktura, FakturaLinje, Pris

admin.site.register(FakturaLinje)
admin.site.register(Pris)


@admin.register(Faktura)
class FakturaAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "bruker",
        "faktura_dato",
        "betalt",
        "sendt",
        Faktura.get_total_sum,
    ]
    list_filter = ["betalt", "sendt"]
