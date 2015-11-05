# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('btp', '0006_auto_20151024_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty',
            name='projectcount',
            field=models.IntegerField(default=0),
        ),
    ]
