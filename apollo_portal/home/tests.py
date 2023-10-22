"""Unit test home application logic."""

from django.conf import settings
from django.core import mail
from django.test import TestCase
from django.test.utils import override_settings

from . import choices, validators
from .forms import ContactForm

VALID_SIGNUP_DATA = {
    'g-recaptcha-response': '1',
    'confirm_institution': 'on',
    'group_name': 'Test group',
    'group_url': '',
    'suggested_hostname': 'testing',
    'name': 'Test User',
    'institution': choices.INSTITUTIONS[1][0],
    'email': 'testing@uq.edu.au',
    'phone': '0499258444',
    'agree_terms': 'on',
    'organism_type': '',
    'list_public': 'True',
    'tracks_public': 'False',
    'grant_type': '',
    'admin_name': 'Test Admin',
    'admin_email': 'admin@uq.edu.au',
}


test_email_backend = (
    'django.core.mail.backends.smtp.EmailBackend'
    if settings.TEST_PRODUCTION_MAIL_SERVER
    else 'django.core.mail.backends.locmem.EmailBackend'
)


def print_form_errors(response):
    """Find and print form errors in HTML - useful for debugging form tests."""
    lines = response.content.decode('utf-8').split('\n')
    if 'errorlist' not in ''.join(lines):
        print('No errors in form HTML')
    for i, line in enumerate(lines):
        if 'errorlist' in line:
            show = '\n'.join(lines[i - 3:i + 3])
            print(show)


class SignupTestCase(TestCase):
    def test_successful_signup(self):
        """Test signup form."""
        response = self.client.post('/signup/', VALID_SIGNUP_DATA)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Thank you for registering')
        self.assertEqual(len(mail.outbox), 3)

    def test_signup_other_institution(self):
        """Test signup form."""
        data = VALID_SIGNUP_DATA.copy()
        data['institution'] = 'Another Institution'
        response = self.client.post('/signup/', data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Thank you for registering')
        self.assertEqual(len(mail.outbox), 3)

    def test_signup_missing_required(self):
        """Test signup form."""
        data = VALID_SIGNUP_DATA.copy()
        data.pop('agree_terms')
        response = self.client.post('/signup/', data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')

    def test_signup_invalid_phone(self):
        """Test signup form."""
        data = VALID_SIGNUP_DATA.copy()
        data['phone'] = '0499258aaa'
        response = self.client.post('/signup/', data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Phone number can only contain numbers')

    def test_signup_invalid_hostname(self):
        """Test signup form."""
        data = VALID_SIGNUP_DATA.copy()
        data['suggested_hostname'] = 'something&invalid'
        response = self.client.post('/signup/', data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hostname can only contain alphanumeric')

    def test_validators(self):
        """Test field validation functions."""
        self.assertEqual(validators.phone_number('0499258444'), None)
        self.assertRaises(validators.ValidationError,
                          validators.phone_number, '0499258aaa')
        self.assertEqual(validators.hostname('testing'), None)
        self.assertRaises(validators.ValidationError,
                          validators.hostname, 'test&invalid')


@override_settings(EMAIL_BACKEND=test_email_backend)
class TestMailServer(TestCase):
    """This test requires a real mail server to be set in .env.test."""

    def test_notify(self):
        """Test submission of mock contact form."""
        form = ContactForm({
            'name': 'Test User',
            'email': 'testuser@example.com',
            'message': 'Test message from Apollo Portal unit tests',
        })
        form.is_valid()
        form.dispatch()
