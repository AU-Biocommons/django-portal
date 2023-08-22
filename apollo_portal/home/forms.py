"""Web forms."""

import logging
import re
from captcha.fields import ReCaptchaField
from django import forms
from .fields import OtherChoiceField
from . import choices, notify

logger = logging.getLogger('django')

BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))


class SignUpForm(forms.Form):
    """Allow users to apply for an Apollo service instance."""

    captcha = ReCaptchaField()
    confirm_institution = forms.BooleanField()
    group_name = forms.CharField(max_length=200)
    group_url = forms.URLField(required=False)
    suggested_hostname = forms.CharField(min_length=4, max_length=200)
    name = forms.CharField(max_length=200)
    institution = OtherChoiceField(choices=choices.INSTITUTIONS)
    email = forms.EmailField()
    phone = forms.CharField(required=False)
    agree_terms = forms.BooleanField()
    organism_type = forms.ChoiceField(
        choices=choices.ORGANISM_TYPES, required=False)
    list_public = forms.ChoiceField(
        choices=BOOL_CHOICES, widget=forms.RadioSelect)
    tracks_public = forms.ChoiceField(
        choices=BOOL_CHOICES, widget=forms.RadioSelect)
    grant_type = forms.ChoiceField(choices=choices.GRANT_TYPES, required=False)
    admin_name = forms.CharField(max_length=200)
    admin_email = forms.EmailField()

    def clean_phone(self):
        data = self.cleaned_data['phone']
        if data is None:
            return data
        stripped = data.replace(' ', '')
        if stripped:
            if re.match(r'^\+?\d+$', stripped):
                raise forms.ValidationError("Phone number must be numeric.")
            if len(stripped) < 9:
                raise forms.ValidationError("Phone number is too short.")
            if stripped[0] not in ('+', '0'):
                raise forms.ValidationError(
                    "Phone number should start with + or 0.")
        return stripped

    def dispatch(self):
        """Send email to Apollo admins and user."""
        notify.user_success(self)
        notify.admin_user_success(self)
        notify.admin(self)
        logger.warning("\n~~~ MOCK SIGNUP DISPATCH ~~~\n")
