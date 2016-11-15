# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0007_celeryresponse'),
    ]

    operations = [
        migrations.AddField(
            model_name='celeryresponse',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 3, 14, 45, 54, 444593)),
        ),
    ]
