"""Web forms."""

import logging
from captcha.fields import ReCaptchaField
from django import forms
from .fields import OtherChoiceField
from . import choices, notify, validators, widgets

logger = logging.getLogger('django')

BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))


class SignUpForm(forms.Form):
    """Allow users to apply for an Apollo service instance."""

    captcha = ReCaptchaField()
    confirm_institution = forms.BooleanField()
    group_name = forms.CharField(max_length=200)
    group_url = forms.URLField(required=False)
    suggested_hostname = forms.CharField(
        min_length=4,
        max_length=200,
        validators=[validators.hostname],
    )
    name = forms.CharField(max_length=200)
    institution = OtherChoiceField(
        choices=choices.INSTITUTIONS,
        widget=widgets.OtherSelect(other_attrs={
            'class': 'form-control',
            'placeholder': 'Please specify your institution',
        }),
    )
    email = forms.EmailField()
    phone = forms.CharField(
        required=False,
        validators=[validators.phone_number],
    )
    agree_terms = forms.BooleanField()
    organism_type = forms.ChoiceField(
        choices=choices.ORGANISM_TYPES,
        required=False,
    )
    list_public = forms.ChoiceField(
        choices=BOOL_CHOICES,
        widget=forms.RadioSelect,
    )
    tracks_public = forms.ChoiceField(
        choices=BOOL_CHOICES,
        widget=forms.RadioSelect,
    )
    grant_type = forms.ChoiceField(choices=choices.GRANT_TYPES, required=False)
    admin_name = forms.CharField(max_length=200)
    admin_email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        """Remove ":" label suffix."""
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    def clean_phone(self):
        return self.cleaned_data['phone'].replace(' ', '')

    def dispatch(self):
        """Send email to Apollo admins and user."""
        notify.user_success(self)
        notify.admin_user_success(self)
        notify.admin(self)
