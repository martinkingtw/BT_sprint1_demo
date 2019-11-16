# Generated by Django 2.2.6 on 2019-11-16 02:29

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('productBacklog', '0001_initial'),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Sprint', max_length=20)),
                ('available_effort', models.IntegerField()),
                ('start_date', models.DateField(blank=True, default=datetime.date(2019, 11, 16), null=True)),
                ('details', models.TextField(null=True)),
                ('project', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Task', max_length=20)),
                ('status', models.CharField(choices=[('To Do', 'To Do'), ('Doing', 'Doing'), ('Done', 'Done')], default='To Do', max_length=5)),
                ('effort', models.IntegerField(verbose_name='effort(hour)')),
                ('details', models.TextField(null=True)),
                ('PBI', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='productBacklog.PBI')),
                ('sprint', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='sprintBacklog.Sprint')),
                ('task_owner', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
