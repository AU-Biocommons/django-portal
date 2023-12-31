# Generated by Django 4.2 on 2023-12-11 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genomes', '0013_alter_genome__metadata_yaml_alter_genome_apollo_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='_metadata_yaml',
            field=models.TextField(blank=True, help_text='Metadata in YAML format. Should be one `key: value` pair per line.', null=True),
        ),
        migrations.AddField(
            model_name='track',
            name='apollo_url',
            field=models.URLField(blank=True, help_text='URL pointing to a public Apollo genome with this track loaded.', null=True),
        ),
        migrations.AddField(
            model_name='track',
            name='condition',
            field=models.CharField(blank=True, help_text='e.g. chemical exposure, genetic manipulation, cancer.', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='track',
            name='description_html',
            field=models.TextField(blank=True, help_text='Description of the genome track with inline HTML. Use `<br>` for a new line and `<a>` tags for links.', null=True),
        ),
        migrations.AddField(
            model_name='track',
            name='doi',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='track',
            name='ncbi_bioproject',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='track',
            name='reference',
            field=models.TextField(blank=True, null=True),
        ),
    ]
