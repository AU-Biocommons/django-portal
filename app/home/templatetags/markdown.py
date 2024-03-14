"""Markdown rendering with python-markdown2.

https://github.com/trentm/python-markdown2
"""

import markdown2
from django import template

register = template.Library()


@register.filter()
def markdown(md):
    """Render html from markdown string."""
    if not md:
        return ""
    return markdown2.markdown(md, extras={
        "tables": None,
        "code-friendly": None,
        "html-classes": {
            'table': 'table table-striped',
        },
    })
