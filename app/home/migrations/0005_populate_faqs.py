"""Migration to populate FAQ entries from JSON data."""

import json
import os
from django.db import migrations


def load_faqs(apps, schema_editor):
    """Load FAQ data from JSON file."""
    FAQ = apps.get_model('home', 'FAQ')
    migration_dir = os.path.dirname(__file__)
    json_path = os.path.join(migration_dir, 'data', 'faqs.json')

    with open(json_path, 'r', encoding='utf-8') as f:
        faqs_data = json.load(f)

    for faq_data in faqs_data:
        FAQ.objects.create(
            question=faq_data['question'].strip(),
            answer=faq_data['answer'].strip(),
            hide=False
        )


def reverse_load_faqs(apps, schema_editor):
    """Remove all FAQ entries."""
    FAQ = apps.get_model('home', 'FAQ')
    FAQ.objects.all().delete()


class Migration(migrations.Migration):
    """Migration to populate FAQ entries."""

    dependencies = [
        ('home', '0004_faq'),
    ]

    operations = [
        migrations.RunPython(load_faqs, reverse_load_faqs),
    ]
