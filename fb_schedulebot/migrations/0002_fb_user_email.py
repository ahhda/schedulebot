# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fb_schedulebot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fb_user',
            name='email',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
    ]
