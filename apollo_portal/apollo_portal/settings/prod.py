"""Production settings."""

import os
from .base import *


SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False
ALLOWED_HOSTS = [
    '127.0.0.1',
    'apollo-portal.genome.edu.au',
    'django-sandpit.genome.edu.au',
]
