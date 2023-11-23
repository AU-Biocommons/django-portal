# Generated by Django 4.2 on 2023-11-23 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0007_lab_apollo_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genome',
            name='accession_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='genome',
            name='apollo_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='genome',
            name='condition',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='genome',
            name='species',
            field=models.CharField(default='None', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='genome',
            name='strain',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='genome',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='genomes'),
        ),
        migrations.AlterField(
            model_name='lab',
            name='apollo_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lab',
            name='description_html',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lab',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='lab',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='labs'),
        ),
        migrations.AlterField(
            model_name='lab',
            name='principle_investigator',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='lab',
            name='website_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='track',
            name='_metadata',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='track',
            name='accession_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
