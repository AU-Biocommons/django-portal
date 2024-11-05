"""Production settings."""

import os
import logging
import sentry_sdk
from .base import *  # noqa: F403
from apollo_portal.utils.environment import is_truthy_string

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False
PRODUCTION_HOSTNAMES = [
    'genome.edu.au',
    'apollo-portal.genome.edu.au',
    'apollo-portal-dev.genome.edu.au',
    'ubuntu22-test.genome.edu.au',
]
ALLOWED_HOSTS += PRODUCTION_HOSTNAMES  # noqa
CSRF_TRUSTED_ORIGINS = [
    f"https://{hostname}"
    for hostname in PRODUCTION_HOSTNAMES
]

TIME_ZONE = 'Australia/Brisbane'

# Use manifest to manage static file versions for cache busting:
STATICFILES_STORAGE = ('django.contrib.staticfiles.storage'
                       '.ManifestStaticFilesStorage')

if not is_truthy_string(os.environ.get('USE_SQLITE_DB')):
    DATABASES['default'] = {  # noqa: F405
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }

sentry_project_id = 'XXX'
sentry_sdk.init(
    dsn=f"https://{sentry_project_id}@sentry.galaxyproject.org/20",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
)
logging.getLogger('sentry_sdk').setLevel(logging.ERROR)
