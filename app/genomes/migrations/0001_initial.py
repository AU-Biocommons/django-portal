# Generated by Django 4.2 on 2023-09-20 23:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('accession_id', models.CharField(max_length=255, null=True)),
                ('name', models.CharField(max_length=255)),
                ('species', models.CharField(max_length=255, null=True)),
                ('strain', models.CharField(max_length=255, null=True)),
                ('condition', models.CharField(max_length=255, null=True)),
                ('thumbnail', models.ImageField(null=True, upload_to='')),
                ('_metadata', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('accession_id', models.CharField(max_length=255, null=True)),
                ('track_type', models.CharField(max_length=255)),
                ('_metadata', models.TextField(null=True)),
                ('genome', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='genomes.genome')),
            ],
        ),
        migrations.AddField(
            model_name='genome',
            name='lab',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='genomes.lab'),
        ),
    ]