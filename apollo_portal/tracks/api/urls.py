"""URLs for tracks API."""

from django.urls import path

from . import endpoints

urlpatterns = [
    path('genomes', endpoints.genomes, name='tracks_api_genomes'),
]
