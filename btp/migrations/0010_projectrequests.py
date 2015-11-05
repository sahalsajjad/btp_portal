# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('btp', '0009_auto_20151102_2119'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectRequests',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project', models.ForeignKey(to='btp.Project')),
                ('submitter', models.ForeignKey(related_name='request_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='request_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
