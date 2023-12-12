from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.genomes, name='genomes_genomes'),
    path('<int:genome_id>/tracks/', views.tracks, name='genomes_tracks'),
    path('api/', include('genomes.api.urls')),
]
