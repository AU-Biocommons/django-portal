"""Custom form widgets."""

from django.forms.widgets import Select


class OtherSelect(Select):
    template_name = 'other_select.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['other_value'] = (
            ''
            if value not in dict(self.choices)
            else value
        )
        return context
