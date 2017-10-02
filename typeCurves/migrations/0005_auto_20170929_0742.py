# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('typeCurves', '0004_auto_20170914_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playproductiondatechoice',
            name='decline',
            field=models.ForeignKey(related_name='playProductionDateChoices', to='typeCurves.PlayProdDecline'),
        ),
        migrations.AlterField(
            model_name='playproductiondatechoice',
            name='play',
            field=models.ForeignKey(related_name='playProductionDateChoices', to='typeCurves.Play'),
        ),
    ]
