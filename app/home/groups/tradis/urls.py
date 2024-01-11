"""Degnan group url patterns."""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tutorial/', views.tutorial, name='tutorial'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]
