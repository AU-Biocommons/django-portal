"""Bulk import Genome records to the database from a JSON file.

Expect JSON:

{
    "lab_name" value,
    "genome_name" value,
    "genome_id" value,  # instead of genome_name
    "name" value,
    "description" value,
    "reference" value,
    "doi" value,
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
from pathlib import Path

from tracks.models import Genome, Lab, Track


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
            self.stdout.write(f"\nImporting {len(data)} track records...")
            input("\nPress ENTER to continue or CTRL+C to cancel\n\n> ")
            for track in data:
                create_track_from_json(track)


def create_track_from_json(track):
    """Create track from given data.

    Create required group and lab records for relational fields.
    """
    if not (track["genome_name"] or track["genome_id"]):
        raise ValueError("Missing required field [genome_name OR genome_id]")
    genome = (
        Genome.objects.filter(name=track["genome_name"]).first()
        if track["genome_name"]
        else Genome.objects.filter(id=track["genome_id"]).first()
    )

    if not track["lab_name"]:
        raise ValueError("Missing required lab_name field")
    lab, _ = Lab.objects.get_or_create(name=track["lab_name"])

    g = Track.objects.create(
        lab=lab,
        genome=genome,
        name=track["name"],
        description_html=track["description"],
        reference=track["reference"],
        doi=track["doi"],
        condition=track["condition"],
        ncbi_bioproject=track["ncbi_bioproject"],
    )

    for k, v in track["metadata"].items():
        g.set_metadata(k, v)
    g.save()

    print(f"Created track {track['name']} in lab {lab.name}")
