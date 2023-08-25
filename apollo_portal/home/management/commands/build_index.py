from django.core.management.base import BaseCommand
from ..import whoosh


class Command(BaseCommand):
    help = 'Index HTML templates with Elasticsearch'

    def handle(self, *args, **kwargs):
        self.stdout.write('')
        count = whoosh.build_index()
        if count:
            self.stdout.write(self.style.SUCCESS(
                f'\nSuccessfully indexed {count} pages\n'))
        else:
            self.stdout.write(self.style.ERROR(
                '\nNo pages were indexed.\n'))
