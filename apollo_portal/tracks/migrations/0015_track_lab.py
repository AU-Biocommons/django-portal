# Generated by Django 4.2 on 2023-12-11 05:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0014_track__metadata_yaml_track_apollo_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='lab',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='tracks.lab'),
            preserve_default=False,
        ),
    ]
