"""Web forms."""

import logging
from captcha.fields import ReCaptchaField
from django import forms
from .fields import OtherChoiceField
from . import choices, notify, validators, widgets

logger = logging.getLogger('django')

BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))


class SubmitDelaySpamFilterMixin(forms.Form):
    """Enforce a submit delay to prevent spam/bot submissions."""

    SUBMIT_DELAY_MINIMUM_SECONDS = 5.0

    submit_delay_seconds = forms.FloatField(
        min_value=SUBMIT_DELAY_MINIMUM_SECONDS)


class HoneypotSpamFilterMixin(forms.Form):
    """Include a honeypot field to catch spam/bot submissions."""

    institution_hp = forms.CharField(required=False)
    honeypot_field = (
        '<input type="text" name="institution_hp" id="id_institution_hp"'
        ' required />\n'
        '<script type="text/javascript">\n'
        'setTimeout('
        '() => $("#id_institution_hp").prop("disabled", true), 2000);\n'
        '$("#id_institution_hp").css("position", "absolute");\n'
        '$("#id_institution_hp").css("opacity", "0");\n'
        '</script>\n')

    def clean_institution_hp(self):
        """Check honeypot field."""
        if self.cleaned_data.get('institution_hf'):
            logger.warning('Honeypot field was filled in.')
            raise forms.ValidationError('This value is incorrect.')
        return self.cleaned_data


class SignUpForm(SubmitDelaySpamFilterMixin, forms.Form):
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
        notify.admins(self)


class ContactForm(
    HoneypotSpamFilterMixin,
    SubmitDelaySpamFilterMixin,
    forms.Form
):
    """Allow users to contact Apollo team."""

    captcha = ReCaptchaField()
    name = forms.CharField(max_length=200)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea, max_length=5000)

    def dispatch(self):
        """Send email to Apollo admins and user."""
        notify.contact_form(self)
        notify.admins(self)
