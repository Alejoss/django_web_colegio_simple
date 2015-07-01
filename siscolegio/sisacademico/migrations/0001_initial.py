# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Alumno'
        db.create_table(u'sisacademico_alumno', (
            ('cedula', self.gf('django.db.models.fields.PositiveIntegerField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('segundo_nombre', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('apellido', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('segundo_apellido', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('sexo', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('num_contacto', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('representante', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('fecha_nacimiento', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('nota_memo', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'sisacademico', ['Alumno'])

        # Adding model 'Matricula'
        db.create_table(u'sisacademico_matricula', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ano_lectivo', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('alumno', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sisacademico.Alumno'])),
            ('nivel', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal(u'sisacademico', ['Matricula'])

        # Adding model 'Nivel'
        db.create_table(u'sisacademico_nivel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal(u'sisacademico', ['Nivel'])

        # Adding model 'Perfil_Profesor'
        db.create_table(u'sisacademico_perfil_profesor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('usuario', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('num_contacto', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('nivel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sisacademico.Nivel'])),
            ('nota_memo', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'sisacademico', ['Perfil_Profesor'])

        # Adding model 'Clase'
        db.create_table(u'sisacademico_clase', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('nivel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sisacademico.Nivel'])),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal(u'sisacademico', ['Clase'])

        # Adding model 'Nota'
        db.create_table(u'sisacademico_nota', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('valor', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('alumno', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sisacademico.Alumno'])),
            ('periodo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sisacademico.Periodo'])),
            ('clase', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sisacademico.Clase'])),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal(u'sisacademico', ['Nota'])

        # Adding model 'Periodo'
        db.create_table(u'sisacademico_periodo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ano', self.gf('django.db.models.fields.IntegerField')()),
            ('quimestre', self.gf('django.db.models.fields.IntegerField')()),
            ('parcial', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'sisacademico', ['Periodo'])


    def backwards(self, orm):
        # Deleting model 'Alumno'
        db.delete_table(u'sisacademico_alumno')

        # Deleting model 'Matricula'
        db.delete_table(u'sisacademico_matricula')

        # Deleting model 'Nivel'
        db.delete_table(u'sisacademico_nivel')

        # Deleting model 'Perfil_Profesor'
        db.delete_table(u'sisacademico_perfil_profesor')

        # Deleting model 'Clase'
        db.delete_table(u'sisacademico_clase')

        # Deleting model 'Nota'
        db.delete_table(u'sisacademico_nota')

        # Deleting model 'Periodo'
        db.delete_table(u'sisacademico_periodo')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sisacademico.alumno': {
            'Meta': {'ordering': "('apellido', 'nombre')", 'object_name': 'Alumno'},
            'apellido': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'cedula': ('django.db.models.fields.PositiveIntegerField', [], {'primary_key': 'True'}),
            'fecha_nacimiento': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'nota_memo': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'num_contacto': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'representante': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'segundo_apellido': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'segundo_nombre': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'sexo': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'sisacademico.clase': {
            'Meta': {'ordering': "('nombre',)", 'object_name': 'Clase'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nivel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sisacademico.Nivel']"}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'sisacademico.matricula': {
            'Meta': {'object_name': 'Matricula'},
            'alumno': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sisacademico.Alumno']"}),
            'ano_lectivo': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nivel': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'sisacademico.nivel': {
            'Meta': {'object_name': 'Nivel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'sisacademico.nota': {
            'Meta': {'object_name': 'Nota'},
            'alumno': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sisacademico.Alumno']"}),
            'clase': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sisacademico.Clase']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'periodo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sisacademico.Periodo']"}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'valor': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'})
        },
        u'sisacademico.perfil_profesor': {
            'Meta': {'ordering': "('usuario',)", 'object_name': 'Perfil_Profesor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nivel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sisacademico.Nivel']"}),
            'nota_memo': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'num_contacto': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'usuario': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'sisacademico.periodo': {
            'Meta': {'object_name': 'Periodo'},
            'ano': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parcial': ('django.db.models.fields.IntegerField', [], {}),
            'quimestre': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['sisacademico']