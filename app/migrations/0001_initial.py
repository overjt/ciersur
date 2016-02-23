# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', null=True, blank=True)),
                ('tipo', models.CharField(max_length=1, choices=[('1', 'Administrador'), ('2', 'Secretaria'), ('3', 'Master Teacher'), ('4', 'Leader Teacher')])),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
        ),
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=1000)),
                ('porcentaje', models.FloatField()),
            ],
            options={
                'verbose_name': 'Actividad',
                'verbose_name_plural': 'Actividades',
            },
        ),
        migrations.CreateModel(
            name='Certificado',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=1, choices=[('A', 'Asistencia'), ('P', 'Participación'), ('E', 'Excelencia')])),
            ],
            options={
                'verbose_name': 'Certificado',
                'verbose_name_plural': 'Certificados',
            },
        ),
        migrations.CreateModel(
            name='Cohorte',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('semestre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.TextField()),
                ('slug', models.SlugField(unique=True, max_length=200)),
            ],
            options={
                'verbose_name': 'Curso',
                'verbose_name_plural': 'Cursos',
            },
        ),
        migrations.CreateModel(
            name='Historial_Academico',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('promocion', models.CharField(max_length=15)),
                ('titulo', models.CharField(max_length=50)),
                ('institucion', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Historial Académico',
                'verbose_name_plural': 'Historiales Académicos',
            },
        ),
        migrations.CreateModel(
            name='Historial_Laboral',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('institucion', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Historial Laboral',
                'verbose_name_plural': 'Historiales Laborales',
            },
        ),
        migrations.CreateModel(
            name='LT_Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('id_curso_cohorte', models.ForeignKey(verbose_name='Curso - Cohorte', to='app.Cohorte')),
                ('id_lt', models.ForeignKey(verbose_name='Cédula del docente', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Curso-LT',
                'verbose_name_plural': 'Cursos-LT',
            },
        ),
        migrations.CreateModel(
            name='MT_Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('id_curso_cohorte', models.ForeignKey(verbose_name='Curso - Cohorte', to='app.Cohorte')),
                ('id_mt', models.ForeignKey(verbose_name='Cédula del docente', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Curso-MT',
                'verbose_name_plural': 'Cursos-MT',
            },
        ),
        migrations.CreateModel(
            name='Nota',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('calificacion', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('id_actividad', models.ForeignKey(verbose_name='Actividad', to='app.Actividad')),
                ('id_lt_curso', models.ForeignKey(verbose_name='LT-Curso', to='app.LT_Curso')),
            ],
            options={
                'verbose_name': 'Nota',
                'verbose_name_plural': 'Notas',
            },
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('cedula', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
                ('apellidos', models.CharField(max_length=200)),
                ('correo', models.CharField(max_length=200, unique=True)),
                ('celular', models.CharField(null=True, max_length=200)),
                ('direccion', models.CharField(null=True, max_length=200)),
                ('fecha_nacimiento', models.DateField()),
                ('sexo', models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')])),
                ('departamento', models.CharField(max_length=3, choices=[('A', 'Amazonas'), ('Caq', 'Caquetá'), ('Ca', 'Cauca'), ('H', 'Huila'), ('N', 'Nariño'), ('P', 'Putumayo'), ('T', 'Tolima'), ('VC', 'Valle del Cauca')])),
                ('ciudad', models.CharField(max_length=15)),
            ],
            options={
                'verbose_name': 'Persona',
                'verbose_name_plural': 'Personas',
            },
        ),
        migrations.CreateModel(
            name='Posible_LT',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('id_curso', models.ForeignKey(verbose_name='Curso', to='app.Curso')),
                ('id_docente', models.ForeignKey(verbose_name='Cédula del docente', to='app.Persona')),
            ],
            options={
                'verbose_name': 'Posible LT',
                'verbose_name_plural': 'Posibles LT',
            },
        ),
        migrations.AddField(
            model_name='historial_laboral',
            name='id_docente',
            field=models.ForeignKey(verbose_name='Cédula del docente', to='app.Persona'),
        ),
        migrations.AddField(
            model_name='historial_academico',
            name='id_docente',
            field=models.ForeignKey(verbose_name='Cédula del docente', to='app.Persona'),
        ),
        migrations.AddField(
            model_name='cohorte',
            name='id_curso',
            field=models.ForeignKey(verbose_name='Curso', to='app.Curso'),
        ),
        migrations.AddField(
            model_name='certificado',
            name='id_lt_curso',
            field=models.OneToOneField(to='app.LT_Curso', verbose_name='LT-Curso'),
        ),
        migrations.AddField(
            model_name='actividad',
            name='id_curso',
            field=models.ForeignKey(verbose_name='Curso', to='app.Curso'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='id_persona',
            field=models.OneToOneField(to='app.Persona', verbose_name='Cédula de la persona'),
        ),
    ]
