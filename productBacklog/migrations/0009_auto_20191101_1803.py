# Generated by Django 2.2.5 on 2019-11-01 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_project_slug'),
        ('productBacklog', '0008_remove_pbis_slug'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PBIs',
            new_name='PBI',
        ),
    ]
