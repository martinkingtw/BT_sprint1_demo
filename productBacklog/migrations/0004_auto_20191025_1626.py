# Generated by Django 2.2.5 on 2019-10-25 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productBacklog', '0003_remove_pbis_itemid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('details', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='pbis',
            name='title',
            field=models.CharField(max_length=20),
        ),
        migrations.AddField(
            model_name='pbis',
            name='project_id',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='productBacklog.Project'),
        ),
    ]
