"""Models for storing generic content."""

from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager
from . import help_text


class User(AbstractUser):
    """Staff user for managing site content."""

    username = None
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        """Return a string representation of self."""
        return f"{self.first_name} {self.last_name} <{self.email}>"


class Notice(models.Model):
    """A site notice to be displayed on the home/landing pages.

    A notice contains a brief message for display on the home page, and a
    longer message that will be linked to on a separate page.

    All notices will shown as rotating - displayed in a top banner and cycled
    through by fade in/out such that multiple notices can be displayed without
    clogging up the UI.
    """

    NOTICE_CLASSES = (
        ('info', 'info'),
        ('warning', 'warning'),
    )

    datetime_modified = models.DateTimeField(auto_now=True)
    notice_class = models.CharField(
        max_length=16, choices=NOTICE_CLASSES, default='',
        help_text=help_text.Notice.NOTICE_CLASS,
    )
    title_html = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        help_text=help_text.Notice.TITLE,
    )
    body_markdown = models.CharField(
        max_length=10000,
        null=True,
        blank=True,
        help_text=help_text.Notice.BODY,
    )
    material_icon = models.CharField(
        max_length=50, null=True, blank=True,
        help_text=help_text.Notice.MATERIAL_ICON,
    )
    enabled = models.BooleanField(
        default=False,
        help_text="Display on the portal landing page."
    )
    is_published = models.BooleanField(
        default=False,
        help_text=(
            "Unpublished content is visible to admin users only."
            " Use this to review content before release to public users."
        ),
    )

    @property
    def timestamp(self):
        """Return timestamp for notice."""
        return self.datetime_modified.isoformat()

    @property
    def url(self):
        """Return the URL for this notice."""
        return f"/notice/{self.id}"

    def __str__(self):
        """Return string representation."""
        return f"[{self.notice_class}] {self.title_html}"

    def clean(self):
        """Clean fields before saving."""
        super().clean()
        if self.material_icon:
            self.material_icon = self.material_icon.lower().replace(' ', '_')
