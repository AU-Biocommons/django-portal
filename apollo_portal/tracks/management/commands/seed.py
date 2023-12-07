"""Seed the database with dummy test data."""

import random
from django.db import transaction
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

from tracks.models import Genome, Lab
from tracks.factories import GenomeFactory, LabFactory

DEFAULT_GENOMES = 50
DEFAULT_LABS = 2  # in addition to Degnan, TraDIS-Vault

CREATE_LABS = [
    "Degnan",
    "Henderson",
    "Vollmer",
]
CREATE_GROUPS = {
    'tradis-vault': [
        CREATE_LABS[1],
        CREATE_LABS[2],
    ]
}


class Command(BaseCommand):
    """Seed the database."""

    help = (
        "Generate fake labs and genomes for testing.\n"
        "WARNING: This will delete all database content!"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "-g",
            "--genomes",
            type=int,
            default=DEFAULT_GENOMES,
            required=False,
            help=("Number of genome records to create"
                  f" (default {DEFAULT_GENOMES})"),
        )
        parser.add_argument(
            "-l",
            "--labs",
            type=int,
            required=False,
            default=DEFAULT_LABS,
            help=("Number of lab records to create"
                  f" (default {DEFAULT_LABS})."),
        )

    @transaction.atomic
    def handle(self, *args, **kwargs):
        """Run the command."""
        input(
            "\nWARNING: This will delete all Group, Lab & Genome records!\n\n"
            "Press ENTER to continue or CTRL+C to cancel\n\n> "
        )

        labs = kwargs["labs"]
        genomes = kwargs["genomes"]
        self.stdout.write("\nDeleting existing Group records...")
        Group.objects.all().delete()
        self.stdout.write("\nDeleting existing Lab & Genome records...")
        Lab.objects.all().delete()

        self.stdout.write(f"\nCreating {labs} Lab records...\n")
        labs = [
            LabFactory()
            for _ in range(labs)
        ]
        for lab_name in CREATE_LABS:
            labs += [LabFactory(name=lab_name)]

        self.stdout.write(f"\nCreating {genomes} Genome records...\n")
        for _ in range(genomes):
            genome = GenomeFactory(lab=random.choice(labs))
            self.stdout.write(f"Created Genome '{genome.name}' under lab"
                              f" '{genome.lab.name}')")

        for name, labs in CREATE_GROUPS.items():
            group = Group.objects.create(name=name)
            for lab_name in labs:
                lab = Lab.objects.get(name=lab_name)
                genomes = Genome.objects.filter(lab=lab)
                for g in genomes:
                    g.group = group
                    g.save()
                    self.stdout.write(f"Assigned genome '{g.name}' to group"
                                      f" '{name}'")
