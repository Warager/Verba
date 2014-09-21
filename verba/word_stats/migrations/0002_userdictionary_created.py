# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('word_stats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdictionary',
            name='created',
            field=models.DateTimeField(default=datetime.date(2014, 9, 21), auto_now_add=True),
            preserve_default=False,
        ),
    ]
