"""Bulk import Genome records to the database from a JSON file.

Expect JSON:

{
    "lab_name" value,
    "genome_name" value,
    "genome_id" value,  # instead of genome_name
    "genome_accession" value,  # instead of genome_name
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

from genomes.models import Genome, Lab, Track


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
    if track.get("genome_name"):
        filter_kwargs = {'name': track["genome_name"]}
    elif track.get("genome_id"):
        filter_kwargs = {'id': track["genome_id"]}
    elif track.get("genome_accession"):
        filter_kwargs = {'accession_id': track["genome_accession"]}
    else:
        raise ValueError(
            "Missing required field"
            " [genome_name OR genome_id OR genome_accession]")

    genome = Genome.objects.filter(**filter_kwargs).first()
    if not genome:
        raise ValueError(
            f"Genome not found for {filter_kwargs}"
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
