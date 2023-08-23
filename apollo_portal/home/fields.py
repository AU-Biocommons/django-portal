"""Custom form fields."""

from django import forms
from .widgets import OtherSelect


class OtherChoiceField(forms.ChoiceField):

    OTHERFIELD_SUFFIX = '__other__'

    def __init__(self, choices=(), widget=OtherSelect, *args, **kwargs):
        choices = list(choices) + [('other', 'Other')]
        super().__init__(choices=choices, widget=widget, *args, **kwargs)

    def other_field_name(self):
        return self.widget.name + self.OTHERFIELD_SUFFIX

    def validate(self, value):
        """Override parent method to fill value from 'other' field."""
        if not value or value == 'other':
            raise forms.ValidationError('This field is required.')
