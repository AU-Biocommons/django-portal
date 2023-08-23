"""Validate form data."""

import re
from django.core.exceptions import ValidationError


def phone_number(value):
    """Validate recognised phone number pattern."""
    if value and not re.match(r'^\+?[\d\-]+$', value.replace(' ', '')):
        raise ValidationError(
            'Phone number can only contain numbers and +/- characters.',
            code="invalid_phone",
        )


def hostname(value):
    """Validate valid subdomain name pattern."""
    if not re.match(r'^[A-z0-9\-]+$', value.replace(' ', '')):
        raise ValidationError(
            "Hostname can only contain alphanumeric and '-' characters",
            code="invalid_hostname",
        )
