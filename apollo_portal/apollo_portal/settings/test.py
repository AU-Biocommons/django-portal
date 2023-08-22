"""Override settings for test environment."""

from .base import *


SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test.db.sqlite3',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
