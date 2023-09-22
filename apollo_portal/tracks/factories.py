"""Model factories for seeding the database."""

import factory
from factory.django import DjangoModelFactory

from . import models


class GenomeFactory(DjangoModelFactory):
    """Generate fake genomes."""

    class Meta:
        model = models.Genome
        django_get_or_create = ('name',)

    lab = factory.SubFactory("tracks.factories.LabFactory")
    name = factory.Faker("word")
    accession_id = factory.Faker("ean8")
    species = factory.Faker("word")
    strain = factory.Faker("word")
    condition = factory.Faker("word")
    thumbnail = factory.django.ImageField(color="blue")
    apollo_url = factory.Faker("url")


class LabFactory(DjangoModelFactory):
    """Generate fake labs."""

    class Meta:
        model = models.Lab
        django_get_or_create = ('name',)

    name = factory.Faker("name")
