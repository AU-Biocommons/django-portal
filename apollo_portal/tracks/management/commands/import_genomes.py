"""Bulk import Genome records to the database from a JSON file.

Expect JSON:

{
    "group_name": value,
    "lab_name" value,
    "name" value,
    "description" value,
    "reference" value,
    "doi" value,
    "strain" value,
    "species" value,
    "condition" value,
    "ncbi_bioproject" value,
    "metadata" value,
        "key": "value",
        ...
    },
}

"""

import json
from django.db import transaction
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from pathlib import Path

from tracks.models import Genome, Lab


class Command(BaseCommand):
    """Seed the database."""

    help = "Bulk import records from a JSON file."

    def add_arguments(self, parser):
        parser.add_argument(
            "-j",
            "--json",
            type=Path,
            help=("Path to JSON to import"),
        )

    @transaction.atomic
    def handle(self, *args, **kwargs):
        """Run the command."""
        with open(kwargs["json"], "r") as f:
            data = json.load(f)
            self.stdout.write(f"\nImporting {len(data)} genome records...")
            input("\nPress ENTER to continue or CTRL+C to cancel\n\n> ")
            for genome in data:
                create_genome_from_json(genome)


def create_genome_from_json(genome):
    """Create genome from given data.

    Create required group and lab records for relational fields.
    """
    if genome["group_name"]:
        group, _ = Group.objects.get_or_create(name=genome["group_name"])
    else:
        group = None
    if genome["lab_name"]:
        lab, _ = Lab.objects.get_or_create(name=genome["lab_name"])
    else:
        lab = None

    g = Genome.objects.create(
        group=group,
        lab=lab,
        name=genome["name"],
        description_html=genome["description"],
        reference=genome["reference"],
        doi=genome["doi"],
        strain=genome["strain"],
        species=genome["species"],
        condition=genome["condition"],
        ncbi_bioproject=genome["ncbi_bioproject"],
    )

    for k, v in genome["metadata"].items():
        g.set_metadata(k, v)
    g.save()

    print(f"Created genome {genome['name']} in lab {lab.name}")
