"""Send mail functions"""

import logging
import time
from datetime import date
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from pprint import pformat

logger = logging.getLogger('django')


def user_success(form):
    """Send confirmation email to user."""
    subject = 'Thank you for registering with the Australian Apollo Service'
    to_address = [form.cleaned_data['email']]
    template = 'home/mail/success_user'
    send_email(form, subject, to_address, template)


def admin_user_success(form):
    """Send confirmation email to user."""
    subject = 'Project Administrator for Apollo Instance'
    to_address = [form.cleaned_data['email']]
    template = 'home/mail/success_admin_user'
    send_email(form, subject, to_address, template)


def admin(form):
    """Send confirmation email to admins."""
    subject = f'Webform submission from: {form.cleaned_data["name"]}'
    to_address = settings.EMAIL_ADMIN_ADDRESSES
    template = 'home/mail/success_admin'
    send_email(form, subject, to_address, template)


def send_email(form, subject, to_address, template):
    """Send email for given form."""
    from_address = settings.EMAIL_FROM_ADDRESS
    context = {
        'form': form,
        'data': form.cleaned_data,
        'today': date.today().strftime('%d-%B-%Y'),
    }
    text = render_to_string(f'{template}.txt', context)
    html = render_to_string(f'{template}.html', context)
    msg = EmailMultiAlternatives(
        subject,
        text,
        from_address,
        to_address,
    )
    msg.attach_alternative(html, "text/html")
    try:
        retry_send(msg)
    except Exception as exc:
        logger.error(
            f'Error sending email:\n{exc}\n\n'
            f'Submitted form values:\n{pformat(form.cleaned_data)}')


def retry_send(msg, retries=3):
    for attempt in range(1, retries + 1):
        try:
            return msg.send()
        except Exception as exc:
            if attempt == retries:
                raise exc
            logging.warning(
                f"Email attempt {attempt} failed."
                " Retrying in 1 second...")
            time.sleep(1)
