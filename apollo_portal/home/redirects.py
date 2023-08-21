"""Redirect old URL paths to something more user-friendly."""

from django.urls import path
from django.shortcuts import redirect

redirect_patterns = [
    path('resources/gettingstarted',
         lambda request: redirect('start', permanent=True)),
    path('resources/termsofuse',
         lambda request: redirect('terms', permanent=True)),
]
