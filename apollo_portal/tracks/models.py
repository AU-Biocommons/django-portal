"""Models for managing Apollo instances and their genome tracks."""

import yaml
from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group


class Lab(models.Model):
    """A research group with an Apollo instance."""

    PLACEHOLDER_STATIC_PATH = 'placeholders/labs/placeholder.png'

    name = models.CharField(max_length=255)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    description_html = models.TextField(null=True, blank=True, help_text=(
        "Description of the genome with inline HTML. Use `<br>` for a new line"
        " and `<a>` tags for links."
    ))
    website_url = models.URLField(null=True, blank=True, help_text=(
        "URL pointing to lab group public website."
    ))
    apollo_url = models.URLField(null=True, blank=True, help_text=(
        "URL pointing to an Apollo login page."
    ))
    principle_investigator = models.CharField(
        max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True, help_text=(
        "Contact email address, if consent has been given to show."
    ))
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

    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    accession_id = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    species = models.CharField(max_length=255)
    strain = models.CharField(max_length=255, null=True, blank=True)
    condition = models.CharField(
        max_length=255, null=True, blank=True, help_text=(
            "e.g. chemical exposure, genetic manipulation, cancer."
        ))
    thumbnail = models.ImageField(null=True, blank=True, upload_to="genomes")
    apollo_url = models.URLField(null=True, blank=True, help_text=(
        "URL pointing to a public Apollo genome/tracks."
    ))
    description_html = models.TextField(null=True, blank=True, help_text=(
        "Description of the genome with inline HTML. Use `<br>` for a new line"
        " and `<a>` tags for links."
    ))
    reference = models.TextField(null=True, blank=True)
    doi = models.CharField(max_length=255, null=True, blank=True)
    ncbi_bioproject = models.CharField(max_length=12, null=True, blank=True)
    _metadata_yaml = models.TextField(null=True, blank=True, help_text=(
        "Metadata in YAML format. Should be one `key: value` pair per line."
    ))

    def __str__(self):
        """Return string representation."""
        return f"{self.lab.name}: {self.name}"

    @property
    def metadata(self):
        """Return metadata as a dictionary."""
        if not self._metadata_yaml:
            return {}
        return yaml.safe_load(self._metadata_yaml)

    def set_metadata(self, k, v):
        """Set metadata key to given value."""
        data = self.metadata
        data[k] = v
        self._metadata_yaml = yaml.safe_dump(data)

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
            "description_html": self.description_html,
            "reference": self.reference,
            "doi": self.doi,
            "ncbi_bioproject": self.ncbi_bioproject,
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

    def __str__(self):
        """Return string representation."""
        return f"{self.genome.lab.name}: {self.genome.name}: {self.name}"
