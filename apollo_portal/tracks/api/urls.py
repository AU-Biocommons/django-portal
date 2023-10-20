"""URLs for tracks API."""

from django.urls import path

from . import endpoints

urlpatterns = [
    path('labs/', endpoints.labs, name='tracks_api_labs'),
    path('genomes/', endpoints.genomes, name='tracks_api_genomes'),
]
