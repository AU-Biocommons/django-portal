from django.contrib import admin

from .admin_forms import NoticeAdminForm
from .models import User, Notice


class NoticeAdmin(admin.ModelAdmin):
    """Administer notices."""

    form = NoticeAdminForm

    class Media:
        """Assets for the admin page."""

        js = (
            '//cdn.jsdelivr.net/simplemde/latest/simplemde.min.js',
            'home/js/admin-required-fields.js',
            'home/js/admin-mde.js',
        )
        css = {
            'screen': (
                '//cdn.jsdelivr.net/simplemde/latest/simplemde.min.css',
                'home/css/admin-mde.css',
            ),
        }

    list_display = [
        'datetime_modified',
        '__str__',
        'enabled',
        'is_published',
    ]
    order = ('-datetime_modified',)


admin.site.register(Notice, NoticeAdmin)
admin.site.register(User)
