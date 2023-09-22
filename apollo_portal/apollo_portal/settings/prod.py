"""Production settings."""

import os
from .base import *  # noqa


SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False
ALLOWED_HOSTS += [  # noqa
    'apollo-portal.genome.edu.au',
    'django-sandpit.genome.edu.au',
]
