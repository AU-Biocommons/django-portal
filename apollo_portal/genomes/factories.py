"""Model factories for seeding the database."""

import factory
from django.conf import settings
from factory.django import DjangoModelFactory

from . import models

FAKE_IMG_DIR = settings.BASE_DIR / "genomes/data/factory/species_images"
FAKE_IMG_INDEX_PATH = FAKE_IMG_DIR / "index.txt"


def _get_fake_image():
    """Return a file handle to a fake image.

    Images are numbered 1-16 with a tracking number in index.txt to ensure that
    images are read sequentially to minimize duplication.
    """
    n = 1
    if FAKE_IMG_INDEX_PATH.exists():
        with open(FAKE_IMG_INDEX_PATH, 'r') as f:
            n = int(f.read().strip(' \n')) + 1
        if n > 16:
            n = 1  # reset the index
    with open(FAKE_IMG_INDEX_PATH, 'w') as f:
        f.write(str(n))

    return open(FAKE_IMG_DIR / f"{n}.png", "rb")


class GenomeFactory(DjangoModelFactory):
    """Generate fake genomes."""

    class Meta:
        model = models.Genome
        django_get_or_create = ('name',)

    lab = factory.SubFactory("genomes.factories.LabFactory")
    name = factory.Faker("word")
    accession_id = factory.Faker("ean8")
    species = factory.Faker("word")
    strain = factory.Faker("ean8")
    condition = factory.Faker("word")
    thumbnail = factory.django.ImageField(from_func=_get_fake_image)
    apollo_url = factory.Faker("url")


class LabFactory(DjangoModelFactory):
    """Generate fake labs."""

    class Meta:
        model = models.Lab
        django_get_or_create = ('name',)

    name = factory.Faker("name")
    description_html = factory.Faker("paragraph")
    website_url = factory.Faker("url")
    email = factory.Faker("email")
    image = factory.django.ImageField(format='PNG')
    principle_investigator = factory.Faker("name")
    apollo_url = factory.Faker("url")
