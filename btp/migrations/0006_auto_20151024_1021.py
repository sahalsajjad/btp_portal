# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('btp', '0005_remove_faculty_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='supervisor',
        ),
        migrations.AddField(
            model_name='project',
            name='supervisor',
            field=models.TextField(default=b'NA'),
        ),
    ]
