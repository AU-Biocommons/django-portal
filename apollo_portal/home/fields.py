"""Custom form fields."""

from django import forms
from .widgets import OtherSelect


class OtherChoiceField(forms.ChoiceField):
    def __init__(self, choices=(), widget=OtherSelect, *args, **kwargs):
        choices = list(choices) + [('other', 'Other')]
        super().__init__(choices=choices, *args, **kwargs)

    def to_python(self, value):
        """Override parent method to fill value from 'other' field."""
        if value == 'other':
            other_field_name = self.name + '_other'
            other_value = self.parent.data.get(other_field_name)
            if not other_value:
                raise forms.ValidationError('This field is required.')
            value = other_value

        return super().to_python(value)
