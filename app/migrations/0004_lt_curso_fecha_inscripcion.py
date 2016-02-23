# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_persona_celular2'),
    ]

    operations = [
        migrations.AddField(
            model_name='lt_curso',
            name='fecha_inscripcion',
            field=models.DateField(default=datetime.datetime(2015, 6, 5, 7, 46, 36, 963264, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
