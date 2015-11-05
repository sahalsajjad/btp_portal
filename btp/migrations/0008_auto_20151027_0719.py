# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('btp', '0007_faculty_projectcount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preference',
            name='partner',
        ),
        migrations.AddField(
            model_name='preference',
            name='partners',
            field=models.TextField(default=b'NA'),
        ),
        migrations.AddField(
            model_name='project',
            name='fileuploaded',
            field=models.FileField(upload_to=b'', blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='isfileuploaded',
            field=models.BooleanField(default=False),
        ),
    ]
