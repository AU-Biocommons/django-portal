"""Add a worker for each available CPU.

Most requests are handled quickly, so 1 worker should be able to handle many
requests per second.
"""

workers = 2

# Environment variables
raw_env = [
    "DJANGO_SETTINGS_MODULE=webapp.settings.prod"
]
