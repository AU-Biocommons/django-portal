from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.genomes, name='tracks_genomes'),
    path('tracks/<int:genome_id>/', views.tracks, name='tracks_tracks'),
    path('api/', include('tracks.api.urls')),
]
