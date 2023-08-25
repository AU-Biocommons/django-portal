"""Production settings."""

import os

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False
ALLOWED_HOSTS += [
    'apollo-portal.genome.edu.au',
    'django-sandpit.genome.edu.au',
]
