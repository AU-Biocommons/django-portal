"""Production settings."""

import os
from .base import *  # noqa


SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False
PRODUCTION_HOSTNAMES = [
    'apollo-portal.genome.edu.au',
    'django-sandpit.genome.edu.au',
]
ALLOWED_HOSTS += PRODUCTION_HOSTNAMES  # noqa
CSRF_TRUSTED_ORIGINS = [
    f"https://{hostname}"
    for hostname in PRODUCTION_HOSTNAMES
]

# Use manifest to manage static file versions for cache busting:
STATICFILES_STORAGE = ('django.contrib.staticfiles.storage'
                       '.ManifestStaticFilesStorage')
