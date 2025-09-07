"""Define Django admin configuration for models."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .admin_forms import NoticeAdminForm, UserCreationForm, UserChangeForm
from .models import User, Notice, FAQ


class UserAdmin(BaseUserAdmin):
    """Administer users."""

    form = UserChangeForm
    add_form = UserCreationForm

    # Remove username field
    ordering = [
        'first_name',
        'last_name',
        'email',
        'password',
        'is_superuser',
        'is_staff',
        'is_active',
        'date_joined',
    ]
    list_display = [
        'first_name',
        'last_name',
        'email',
    ]
    list_filter = ['is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
        ('Personal', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': (
                'is_staff',
                'is_superuser',
                'is_active',
                'user_permissions',
        )}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
        ('Personal', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': (
                'is_staff',
                'is_superuser',
                'is_active',
                'user_permissions',
        )}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


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


class FAQAdmin(admin.ModelAdmin):
    """Administer FAQs."""

    list_display = [
        'question',
        'hide',
    ]


admin.site.register(User, UserAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(FAQ, FAQAdmin)
