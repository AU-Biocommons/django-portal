"""Custom form widgets."""

from django.forms.widgets import Select


class OtherSelect(Select):
    template_name = 'home/widgets/other_select.html'

    def __init__(self, other_attrs={}, **kwargs):
        self.other_attrs = other_attrs
        super().__init__(**kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['other_value'] = (
            value
            if value not in dict(self.choices)
            else ''
        )
        context['widget']['other_attrs'] = self.other_attrs
        return context
