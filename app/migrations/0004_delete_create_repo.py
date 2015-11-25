# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_create_repo'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Create_repo',
        ),
    ]
