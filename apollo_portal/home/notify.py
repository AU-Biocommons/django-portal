"""Send mail functions"""

import logging
import time
import traceback
from datetime import date
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from pprint import pformat

from apollo_portal.utils import postal

logger = logging.getLogger('django')


def user_success(form):
    """Send confirmation email to user."""
    subject = 'Thank you for registering with the Australian Apollo Service'
    to_addresses = [form.cleaned_data['email']]
    template = 'home/mail/success_user'
    send_email(form, subject, to_addresses, template)


def admin_user_success(form):
    """Send confirmation email to admin user."""
    subject = 'Project Administrator for Apollo Instance'
    to_addresses = [form.cleaned_data['admin_email']]
    template = 'home/mail/success_admin_user'
    send_email(form, subject, to_addresses, template)


def contact_form(form):
    """Send contact form email to admins."""
    subject = 'We have received your message'
    to_addresses = [form.cleaned_data['email']]
    template = 'home/mail/contact_confirmation'
    send_email(form, subject, to_addresses, template)


def admins(form):
    """Email submitted form content to admins."""
    subject = f'Apollo webform submission from: {form.cleaned_data["name"]}'
    to_addresses = [settings.EMAIL_TO_ADDRESS]
    template = 'home/mail/success_admin'
    send_email(form, subject, to_addresses, template)


def send_email(form, subject, to_addresses, template):
    """Send email for given form."""
    logger.info(f'Sending email to {to_addresses} Subject: {subject}')
    from_address = settings.EMAIL_FROM_ADDRESS
    context = {
        'today': date.today().strftime('%d-%m-%Y'),
        'data': {
            field.name: {
                'label': field.label,
                'value': form.cleaned_data[field.name],
            }
            for field in form
            if field.name not in ['captcha', 'submit_delay_seconds']
        },
    }

    text = render_to_string(f'{template}.txt', context)
    html = render_to_string(f'{template}.html', context)
    msg = EmailMultiAlternatives(
        subject,
        text,
        from_address,
        to_addresses,
    )
    msg.attach_alternative(html, "text/html")
    try:
        retry_send(msg)
    except Exception:
        logger.error(
            f'Error sending email:\n{traceback.format_exc()}\n\n'
            f'Submitted form values:\n{pformat(form.cleaned_data)}')


def retry_send(msg, retries=3):
    for attempt in range(1, retries + 1):
        try:
            if settings.EMAIL_HOST == 'mail.usegalaxy.org.au':
                return postal.send_mail(msg)
            return msg.send()
        except Exception as exc:
            if attempt == retries:
                raise exc
            logging.warning(
                f"Email attempt {attempt} failed."
                " Retrying in 1 second...")
            time.sleep(1)
