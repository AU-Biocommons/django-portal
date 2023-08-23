"""Custom form widgets."""

from django.forms.widgets import Select


class OtherSelect(Select):
    template_name = 'home/widgets/other_select.html'

    def __init__(self, other_attrs={}, **kwargs):
        self.other_attrs = other_attrs
        super().__init__(**kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        if value not in dict(self.choices):
            # Set the other field to selected:
            group_name, group_choices, group_index = (
                context['widget']['optgroups'][-1]
            )
            context['widget']['optgroups'][-1] = (
                group_name, [
                    {
                        **group_choices[0],
                        'selected': True,
                        'attrs': {'selected': True},
                    }
                ], group_index)

            # Set the other_value to whatever value is set:
            context['widget']['other_value'] = value

        context['widget']['other_attrs'] = self.other_attrs
        return context
