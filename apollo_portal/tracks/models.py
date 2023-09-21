"""Models for managing Apollo instances and their genome tracks."""

import json
from django.db import models


class Lab(models.Model):
    """A research group with an Apollo instance."""

    name = models.CharField(max_length=255)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)


class Genome(models.Model):
    """Represents a genome reference on an Apollo instance."""

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    accession_id = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255)
    species = models.CharField(max_length=255, null=True)
    strain = models.CharField(max_length=255, null=True)
    condition = models.CharField(max_length=255, null=True)
    thumbnail = models.ImageField(null=True, upload_to="genomes")
    _metadata = models.TextField(null=True)

    @property
    def metadata(self):
        """Return metadata as a dictionary."""
        return json.loads(self._metadata)

    @property
    def set_metadata(self, k, v):
        """Set metadata key to given value."""
        data = json.loads(self._metadata)
        data[k] = v
        self._metadata = json.dumps(data)


class Track(models.Model):
    """A track mapped to a genome reference.

    Not currently used but maybe in future.

    Should probably defer to an embedded "Machado" instance for tracks:
    https://www.machado.cnptia.embrapa.br/demo_machado

    """

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    genome = models.ForeignKey(Genome, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    accession_id = models.CharField(max_length=255, null=True)
    track_type = models.CharField(max_length=255)
    _metadata = models.TextField(null=True)

    @property
    def metadata(self):
        """Return metadata as a dictionary."""
        return json.loads(self._metadata)

    @property
    def set_metadata(self, k, v):
        """Set metadata key to given value."""
        data = json.loads(self._metadata)
        data[k] = v
        self._metadata = json.dumps(data)
