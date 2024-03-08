from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .admin_forms import UserCreationForm, UserChangeForm
from .models import User


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


admin.site.register(User, UserAdmin)
