# Generated by Django 4.2 on 2023-09-28 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0005_lab_description_html_lab_email_lab_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lab',
            name='principle_investigator',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
