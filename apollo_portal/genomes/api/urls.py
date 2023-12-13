"""URLs for tracks API."""

from django.urls import path

from . import endpoints

urlpatterns = [
    path('labs/', endpoints.labs, name='genomes_api_labs'),
    path('genomes/', endpoints.genomes, name='genomes_api_genomes'),
    path('tracks/', endpoints.tracks, name='genomes_api_tracks'),
]
