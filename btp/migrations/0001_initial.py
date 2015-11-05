# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(max_length=20)),
                ('event', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('startdate', models.DateField()),
                ('enddate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('institute', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('supervisor', models.CharField(max_length=100)),
                ('skillset', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('summer', models.CharField(default=b'04', max_length=5, choices=[(b'01', b"Must work on this project in summer, and you'll be paid"), (b'02', b"Must work on this project in summer, but you'll not be paid"), (b'03', b"May have to work in summer, can't say at this time"), (b'04', b'You dont have to work during summer')])),
                ('taken', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('branch', models.CharField(max_length=5)),
                ('rollno', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='postedby',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='preference',
            name='partner',
            field=models.ForeignKey(related_name='project_partner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='preference',
            name='pref1',
            field=models.ForeignKey(related_name='project_preference_1', to='btp.Project'),
        ),
        migrations.AddField(
            model_name='preference',
            name='pref2',
            field=models.ForeignKey(related_name='project_preference_2', to='btp.Project'),
        ),
        migrations.AddField(
            model_name='preference',
            name='pref3',
            field=models.ForeignKey(related_name='project_preference_3', to='btp.Project'),
        ),
        migrations.AddField(
            model_name='preference',
            name='student',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
