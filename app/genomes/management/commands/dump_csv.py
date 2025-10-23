"""Dump model data to CSV file."""

import csv
from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Export data from Genome models in CSV format'

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str,
                            help='Name of the model to export')
        parser.add_argument('-o', '--outfile', type=str,
                            help='Output file path')

    def handle(self, *args, **kwargs):
        model_name = kwargs['model_name']
        Model = apps.get_model('genomes', model_name.capitalize())
        filename = kwargs.get('outfile', f'{model_name}.csv')
        field_names = [field.name for field in Model._meta.fields]

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(field_names)
            for obj in Model.objects.all():
                writer.writerow([getattr(obj, field) for field in field_names])

        self.stdout.write(
            self.style.SUCCESS(
                f'Data from {model_name} exported successfully to {filename}.'
            )
        )
