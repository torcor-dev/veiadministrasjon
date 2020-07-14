from django.urls import path
from .views import HytteListView

urlpatterns = [
        path('', HytteListView.as_view(), name='Hytteliste'),
        ]
