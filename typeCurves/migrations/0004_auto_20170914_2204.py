# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('typeCurves', '0003_auto_20170914_2110'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playproddecline',
            old_name='prod_decline',
            new_name='prod',
        ),
        migrations.AddField(
            model_name='playproductiondatechoice',
            name='decline',
            field=models.ForeignKey(related_name='playProductionDateChoices', default=1, to='typeCurves.PlayProdDecline'),
        ),
        migrations.AddField(
            model_name='playproductiondatechoice',
            name='play',
            field=models.ForeignKey(related_name='playProductionDateChoices', default=1, to='typeCurves.Play'),
        ),
    ]
