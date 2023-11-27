"""Models for managing Apollo instances and their genome tracks."""

import json
from django.db import models
from django.conf import settings


class Lab(models.Model):
    """A research group with an Apollo instance."""

    PLACEHOLDER_STATIC_PATH = 'placeholders/labs/placeholder.png'

    name = models.CharField(max_length=255)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    description_html = models.TextField(null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)
    apollo_url = models.URLField(null=True, blank=True)
    principle_investigator = models.CharField(
        max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="labs")

    def __str__(self):
        """Return string representation."""
        return self.name

    @property
    def img_path_or_placeholder(self):
        """Return image path or placeholder if not set."""
        return (
            self.image.url
            if self.image
            else settings.STATIC_URL + self.PLACEHOLDER_STATIC_PATH
        )

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
            "image": self.img_path_or_placeholder,
        }


class Genome(models.Model):
    """Represents a genome reference on an Apollo instance.

    Genomes has several publicity states:

    - Public: Apollo accessible to all users and can edit
    - Public readonly: Apollo accessible to all users
    - Private: Apollo requires login but is listed on portal
        - public users might like to request access/collaboration?

    """

    PLACEHOLDER_STATIC_PATH = "placeholders/genomes/placeholder.png"

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    accession_id = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    species = models.CharField(max_length=255)
    strain = models.CharField(max_length=255, null=True, blank=True)
    condition = models.CharField(max_length=255, null=True, blank=True)
    thumbnail = models.ImageField(null=True, blank=True, upload_to="genomes")
    apollo_url = models.URLField(null=True, blank=True)
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
            "thumbnail": self.img_path_or_placeholder,
            "apollo_url": self.apollo_url,
            "metadata": self.metadata,
        }

    @property
    def img_path_or_placeholder(self):
        """Return image path or placeholder if not set."""
        return (
            self.thumbnail.url
            if self.thumbnail
            else settings.STATIC_URL + self.PLACEHOLDER_STATIC_PATH
        )


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
    accession_id = models.CharField(max_length=255, null=True, blank=True)
    track_type = models.CharField(max_length=255)
    _metadata = models.TextField(null=True, blank=True)

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
