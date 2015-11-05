# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('btp', '0010_projectrequests'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='fileuploaded',
            field=models.FileField(null=True, upload_to=b'', blank=True),
        ),
    ]
