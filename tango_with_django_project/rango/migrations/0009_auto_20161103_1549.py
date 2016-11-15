# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0008_celeryresponse_timestamp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='celeryresponse',
            name='timestamp',
        ),
        migrations.AlterField(
            model_name='celeryresponse',
            name='message',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
