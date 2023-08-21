"""Build Elasticsearch index for HTML templates."""

from django.core.management.base import BaseCommand
from elasticsearch import Elasticsearch
import os


class Command(BaseCommand):
    help = 'Index HTML templates to Elasticsearch'

    def handle(self, *args, **kwargs):
        es = Elasticsearch()

        # Define the index structure
        mapping = {
            "mappings": {
                "properties": {
                    "content": {"type": "text"},
                    "url": {"type": "keyword"}
                }
            }
        }

        # Create the index
        index_name = 'django_templates'
        es.indices.create(index=index_name, body=mapping, ignore=400)

        # Directory where templates are located
        templates_dir = os.path.join(
            os.path.dirname(__file__),
            'path/to/your/templates')

        # Iterate through the HTML files
        for filename in os.listdir(templates_dir):
            if filename.endswith('.html'):
                filepath = os.path.join(templates_dir, filename)

                # Extract content
                with open(filepath, 'r') as file:
                    content = file.read()

                # Define the URL mapping
                url_path = f'/path/to/{filename}'

                # Index the document
                doc = {'content': content, 'url': url_path}
                es.index(index=index_name, document=doc)

        self.stdout.write(self.style.SUCCESS('Successfully indexed templates'))
