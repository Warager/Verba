# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('word_stats', '0002_userdictionary_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdictionary',
            name='created',
            field=models.DateTimeField(auto_now_add=True,
                                       verbose_name=b'created'),
        ),
    ]
