from django.urls import path
from . import views

urlpatterns = [
    path('', views.organisms, name='tracks_organisms'),
]
