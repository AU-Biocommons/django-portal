from django.urls import path
from .redirects import redirect_patterns
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('resources/start',
         views.getting_started,
         name='getting_started'),
    path('resources/terms', views.terms, name='terms'),
] + redirect_patterns
