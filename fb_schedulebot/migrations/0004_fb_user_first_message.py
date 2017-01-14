# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fb_schedulebot', '0003_fb_user_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='fb_user',
            name='first_message',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
