# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('btp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='email',
        ),
        migrations.AlterField(
            model_name='project',
            name='postedby',
            field=models.ForeignKey(related_name='project_postedby', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='project',
            name='supervisor',
        ),
        migrations.AddField(
            model_name='project',
            name='supervisor',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
