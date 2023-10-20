"""Functions for configuring environment."""


def is_truthy_string(value):
    """Return True if value is a truthy string."""
    return str(value).lower() in ('true', '1', 'yes', 'y')
