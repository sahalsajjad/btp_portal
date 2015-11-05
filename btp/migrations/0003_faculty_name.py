# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('btp', '0002_auto_20151023_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty',
            name='name',
            field=models.CharField(default=models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL), max_length=200),
        ),
    ]
