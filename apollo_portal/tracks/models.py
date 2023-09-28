"""Models for managing Apollo instances and their genome tracks."""

import json
from django.db import models


class Lab(models.Model):
    """A research group with an Apollo instance."""

    name = models.CharField(max_length=255)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    description_html = models.TextField(null=True)
    website_url = models.URLField(null=True)
    apollo_url = models.URLField(null=True)
    principle_investigator = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    image = models.ImageField(null=True, upload_to="labs")

    def __str__(self):
        """Return string representation."""
        return self.name

    def as_json(self):
        """Serialize model for JSON encoding."""
        return {
            "id": self.id,
            "created": self.datetime_created.isoformat(),
            "modified": self.datetime_modified.isoformat(),
            "name": self.name,
            "description_html": self.description_html,
            "website_url": self.website_url,
            "apollo_url": self.apollo_url,
            "principle_investigator": self.principle_investigator,
            "email": self.email,
            "image": self.image.url if self.image else None,
        }


class Genome(models.Model):
    """Represents a genome reference on an Apollo instance.

    Genomes has several publicity states:

    - Public: Apollo accessible to all users and can edit
    - Public readonly: Apollo accessible to all users
    - Private: Apollo requires login but is listed on portal
        - public users might like to request access/collaboration?

    """

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    accession_id = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255)
    species = models.CharField(max_length=255, null=True)
    strain = models.CharField(max_length=255, null=True)
    condition = models.CharField(max_length=255, null=True)
    thumbnail = models.ImageField(null=True, upload_to="genomes")
    apollo_url = models.URLField(null=True)
    _metadata = models.TextField(default="{}")

    def __str__(self):
        """Return string representation."""
        return f"{self.lab.name}: {self.name}"

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

    def as_json(self):
        """Serialize model for JSON encoding."""
        return {
            "id": self.id,
            "created": self.datetime_created.isoformat(),
            "modified": self.datetime_modified.isoformat(),
            "accession_id": self.accession_id,
            "lab": self.lab.name,
            "name": self.name,
            "species": self.species,
            "strain": self.strain,
            "condition": self.condition,
            "thumbnail": self.thumbnail.url if self.thumbnail else None,
            "apollo_url": self.apollo_url,
            "metadata": self.metadata,
        }


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

    def __str__(self):
        """Return string representation."""
        return f"{self.genome.lab.name}: {self.genome.name}: {self.name}"

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
