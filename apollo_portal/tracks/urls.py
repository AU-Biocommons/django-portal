from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.genomes, name='tracks_genomes'),
    path('genomes/', views.genomes, name='tracks_genomes'),
    path('api/', include('tracks.api.urls')),
]
