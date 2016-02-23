# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_lt_curso_fecha_inscripcion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificado',
            name='id',
        ),
        migrations.AddField(
            model_name='lt_curso',
            name='aprobado',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AlterField(
            model_name='certificado',
            name='id_lt_curso',
            field=models.OneToOneField(primary_key=True, serialize=False, verbose_name='LT-Curso', to='app.LT_Curso'),
        ),
    ]
