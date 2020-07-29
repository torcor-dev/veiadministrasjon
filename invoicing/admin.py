from django.contrib import admin
from .models import Faktura, FakturaLinje, Pris

admin.site.register(Faktura)
admin.site.register(FakturaLinje)
admin.site.register(Pris)

# Register your models here.
