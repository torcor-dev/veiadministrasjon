from django.shortcuts import render
from django.views.generic import ListView
from .models import Bruker, Hytte, Poststed, Faktura

class HytteListView(ListView):
    model = Hytte
    context_object_name = 'hytter'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx
