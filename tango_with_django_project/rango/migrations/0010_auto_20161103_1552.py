# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0009_auto_20161103_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='celeryresponse',
            name='message',
            field=models.CharField(max_length=255),
        ),
    ]
