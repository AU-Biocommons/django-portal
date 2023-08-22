"""Production settings."""

import os

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False
ALLOWED_HOSTS.append('apollo-portal.genome.edu.au')
