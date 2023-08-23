"""Degnan group url patterns."""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cots', views.cots, name='cots'),
    path('amphimedon', views.amphimedon, name='amphimedon'),
]
