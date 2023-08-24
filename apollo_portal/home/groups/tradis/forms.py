"""Tradis-vault forms."""

from captcha.fields import ReCaptchaField
from django import forms

from . import notify


class ContactForm(forms.Form):
    """Tradis-vault contact form."""

    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='Email')
    subject = forms.CharField(max_length=200, label='Subject')
    message = forms.CharField(
        max_length=2000,
        label='Message',
        widget=forms.Textarea(attrs={'rows': 5}),
    )
    captcha = ReCaptchaField()

    def dispatch(self):
        """Dispatch the form."""
        notify.contact_admin(self)
        notify.contact_user(self)
