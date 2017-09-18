# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navProved', '0017_auto_20170914_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayProdDecline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('play', models.ForeignKey(related_name='playProdDeclines', to='navProved.Play')),
                ('prod', models.ForeignKey(related_name='playProdDeclines', to='navProved.PlayProduction')),
                ('ticker', models.ForeignKey(related_name='playProdDeclines', to='navProved.Ticker')),
            ],
        ),
        migrations.RenameField(
            model_name='playproductiondatechoice',
            old_name='production',
            new_name='prod',
        ),
    ]
