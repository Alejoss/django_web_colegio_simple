# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('cedula', models.PositiveIntegerField(serialize=False, primary_key=True, validators=[django.core.validators.MaxValueValidator(9999999999)])),
                ('nombre', models.CharField(max_length=150)),
                ('segundo_nombre', models.CharField(max_length=150, blank=True)),
                ('apellido', models.CharField(max_length=150)),
                ('segundo_apellido', models.CharField(max_length=150, blank=True)),
                ('sexo', models.CharField(max_length=20, choices=[(b'M', b'masculino'), (b'F', b'femenino')])),
                ('num_contacto', models.IntegerField(null=True, blank=True)),
                ('representante', models.CharField(max_length=150, blank=True)),
                ('fecha_nacimiento', models.DateField(null=True, blank=True)),
                ('status', models.CharField(max_length=150, choices=[(b'A', b'Activo'), (b'I', b'Inactivo')])),
                ('nota_memo', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('apellido', 'nombre'),
            },
        ),
        migrations.CreateModel(
            name='Clase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=250)),
                ('descripcion', models.CharField(max_length=1000, null=True, blank=True)),
                ('status', models.CharField(max_length=150, choices=[(b'A', b'Activo'), (b'I', b'Inactivo')])),
            ],
            options={
                'ordering': ('nombre',),
            },
        ),
        migrations.CreateModel(
            name='Clase_Profesor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('clase', models.ForeignKey(blank=True, to='sisacademico.Clase', null=True)),
            ],
            options={
                'ordering': ('profesor',),
                'verbose_name': 'Profesor de Clase',
                'verbose_name_plural': 'Profesores de cada clase',
            },
        ),
        migrations.CreateModel(
            name='Matricula',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ano_lectivo', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(9999)])),
                ('status', models.CharField(max_length=150, choices=[(b'A', b'Activo'), (b'I', b'Inactivo')])),
                ('alumno', models.ForeignKey(to='sisacademico.Alumno')),
            ],
            options={
                'ordering': ('alumno',),
                'verbose_name': 'matr\xedcula',
                'verbose_name_plural': 'matr\xedculas',
            },
        ),
        migrations.CreateModel(
            name='Nivel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'niveles',
            },
        ),
        migrations.CreateModel(
            name='Nota',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('valor', models.DecimalField(null=True, max_digits=4, decimal_places=2, blank=True)),
                ('tipo', models.CharField(max_length=150)),
                ('publicada', models.BooleanField(default=True)),
                ('alumno', models.ForeignKey(to='sisacademico.Alumno')),
                ('clase', models.ForeignKey(to='sisacademico.Clase')),
            ],
        ),
        migrations.CreateModel(
            name='Perfil_Profesor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=250, blank=True)),
                ('num_contacto', models.IntegerField(null=True, blank=True)),
                ('status', models.CharField(max_length=150, choices=[(b'A', b'Activo'), (b'I', b'Inactivo')])),
                ('nota_memo', models.TextField(blank=True)),
                ('nivel', models.ForeignKey(blank=True, to='sisacademico.Nivel', null=True)),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-usuario',),
                'verbose_name': 'perfil de profesor',
                'verbose_name_plural': 'perfiles de profesores',
            },
        ),
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ano_lectivo', models.CharField(max_length=150, blank=True)),
                ('quimestre', models.IntegerField()),
                ('parcial', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='nota',
            name='periodo',
            field=models.ForeignKey(to='sisacademico.Periodo'),
        ),
        migrations.AddField(
            model_name='matricula',
            name='nivel',
            field=models.ForeignKey(to='sisacademico.Nivel', null=True),
        ),
        migrations.AddField(
            model_name='clase_profesor',
            name='profesor',
            field=models.ForeignKey(blank=True, to='sisacademico.Perfil_Profesor', null=True),
        ),
        migrations.AddField(
            model_name='clase',
            name='nivel',
            field=models.ForeignKey(to='sisacademico.Nivel'),
        ),
    ]
