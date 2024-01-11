"""Email notifications on form submission."""

from django.conf import settings

from home.notify import send_email


def contact_admin(form):
    """Send confirmation email to admin."""
    subject = (
        f'TraDIS-Vault contact submission from:'
        f' {form.cleaned_data["name"]}')
    to_addresses = [settings.EMAIL_TO_ADDRESS, 'services@qcif.edu.au']
    template = 'home/groups/tradis/mail/contact'
    send_email(form, subject, to_addresses, template)


def contact_user(form):
    """Send confirmation email to user."""
    subject = ('TraDIS-Vault email confirmation')
    to_addresses = [form.cleaned_data["email"]]
    template = 'home/groups/tradis/mail/contact-user'
    send_email(form, subject, to_addresses, template)
