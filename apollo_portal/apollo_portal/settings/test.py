"""Override settings for test environment."""

import os
from dotenv import load_dotenv

from apollo_portal.utils.environment import is_truthy_string
from .base import *  # noqa: F403

env_file = BASE_DIR.parent / '.env.test'  # noqa: F405
if env_file.exists():
    load_dotenv(env_file, override=True)

TEST_PRODUCTION_MAIL_SERVER = is_truthy_string(
    os.environ.get('TEST_PRODUCTION_MAIL_SERVER'))

SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test.db.sqlite3',  # noqa: F405
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
if TEST_PRODUCTION_MAIL_SERVER:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ.get('MAIL_HOSTNAME')
    EMAIL_PORT = os.environ.get('MAIL_SMTP_PORT')
    EMAIL_HOST_USER = os.environ.get('MAIL_SMTP_USERNAME')
    EMAIL_HOST_PASSWORD = os.environ.get('MAIL_SMTP_PASSWORD')
    EMAIL_USE_TLS = (
        str(os.environ.get('MAIL_USE_TLS')).lower()
        in ('1', 'true')
    )
    EMAIL_FROM_ADDRESS = os.environ.get('MAIL_FROM_ADDRESS')
    EMAIL_TO_ADDRESS = os.environ.get('MAIL_TO_ADDRESS')
    SERVER_EMAIL = os.environ.get('MAIL_FROM_ADDRESS')

# Google's test keys always pass validation
RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'

LOGGING['loggers']['django']['level'] = 'ERROR'  # noqa: F405
