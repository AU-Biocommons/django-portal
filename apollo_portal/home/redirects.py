"""Redirect old URL paths to something more user-friendly."""

from django.urls import path
from django.shortcuts import redirect

REDIRECT_PATHS = {
     'gettingstarted': '/resources/start',
     'userdocumentationandtutorials': '/resources/documentation',
     'trainingandhelpresources': '/resources/training',
     'node/27': '/resources/faqs',
     'video': '/resources/video',
     'termsofuse': '/resources/terms',
     'form/signup': '/signup',
     'resources': '/',
}


def get_redirect(old_path):
    """Return a redirect function for an old path."""
    return lambda request: redirect(REDIRECT_PATHS[old_path], permanent=True)


redirect_patterns = [
    path(p, get_redirect(p))
    for p in REDIRECT_PATHS
]
