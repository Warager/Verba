# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0003_auto_20140922_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdictionary',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
