"""Model event hooks."""

from django.db.models.signals import post_save

from .models import Lab, Track


@post_save(sender=Track)
def delete_track_image(sender, instance, **kwargs):
    """Delete track image on track deletion."""
    if instance.image:
        instance.image.delete(save=False)


@post_save(sender=Lab)
def delete_lab_image(sender, instance, **kwargs):
    """Delete lab image on lab deletion."""
    if instance.image:
        instance.image.delete(save=False)
