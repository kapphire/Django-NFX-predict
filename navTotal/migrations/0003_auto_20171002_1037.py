# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navTotal', '0002_totalequityoffering'),
    ]

    operations = [
        migrations.RenameField(
            model_name='totalequityoffering',
            old_name='chocie',
            new_name='choice',
        ),
    ]
