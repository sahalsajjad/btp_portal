# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('btp', '0008_auto_20151027_0719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(default=b'NA'),
        ),
        migrations.AlterField(
            model_name='project',
            name='skillset',
            field=models.TextField(default=b'NA'),
        ),
    ]
