# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fb_schedulebot', '0002_fb_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='fb_user',
            name='label',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
