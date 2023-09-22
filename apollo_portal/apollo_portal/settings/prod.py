"""Production settings."""

import os
from .base import *  # noqa


SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False
ALLOWED_HOSTS += [  # noqa
    'apollo-portal.genome.edu.au',
    'django-sandpit.genome.edu.au',
]

# Use manifest to manage static file versions for cache busting:
STATICFILES_STORAGE = ('django.contrib.staticfiles.storage'
                       '.ManifestStaticFilesStorage')
