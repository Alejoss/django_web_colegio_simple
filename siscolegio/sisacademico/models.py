# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Alumno(models.Model):
	cedula = models.PositiveIntegerField(primary_key=True)
	nombre = models.CharField(max_length=150)
	segundo_nombre = models.CharField(max_length=150, blank=True)
	apellido = models.CharField(max_length=150)
	segundo_apellido = models.CharField(max_length=150, blank=True)
	sexo = models.CharField(max_length=20, choices=(("M", "masculino"), ("F", "femenino")))
	num_contacto = models.IntegerField(null=True, blank=True)
	representante = models.CharField(max_length=150, blank=True)
	fecha_nacimiento = models.DateField(blank=True, null=True)
	status = models.CharField(max_length=150, choices=(("A", "Activo"), ("I", "Inactivo")))
	nota_memo = models.TextField(blank=True)

	class Meta:
		ordering = ("apellido", "nombre")

	def __unicode__(self):
		return u"%s %s" % (self.nombre, self.apellido)

	@property
	def nombre_completo(self):
		return "{0} {1} {2} {3}".format(self.nombre, self.segundo_nombre,
			                            self.apellido, self.segundo_apellido)

	@property
	def datos_contacto(self):
		return [self.num_contacto, self.representante]


class Nivel(models.Model):
	"""
	Ej - "Octavo de Básica, 6to Curso"
	"""
	nombre = models.CharField(max_length=150)

	class Meta:
		verbose_name_plural = "niveles"

	def __unicode__(self):
		return self.nombre


class Matricula(models.Model):
	ano_lectivo = models.PositiveIntegerField()
	alumno = models.ForeignKey(Alumno)
	nivel = models.ForeignKey(Nivel, null=True)
	status = models.CharField(max_length=150, choices=(("A", "Activo"), ("I", "Inactivo")))

	class Meta:
		verbose_name_plural = "matrículas"
		verbose_name = "matrícula"

	def __unicode__(self):
		return u"Matricula %s %s" % (self.alumno, self.ano_lectivo)


class Perfil_Profesor(models.Model):
	usuario = models.OneToOneField(User)
	titulo = models.CharField(max_length=250, blank=True)
	num_contacto = models.IntegerField(null=True, blank=True)
	status = models.CharField(max_length=150, choices=(("A", "Activo"), ("I", "Inactivo")))
	nivel = models.ForeignKey(Nivel, null=True, blank=True)
	nota_memo = models.TextField(blank=True)

	class Meta:
		ordering = ("usuario",)
		verbose_name = "perfil de profesor"
		verbose_name_plural = "perfiles de profesores"

	def __unicode__(self):
		return "%s %s" % (self.usuario.first_name, self.usuario.last_name)

	@property
	def status_activo(self):
		if self.status == "Activo":
			return True
		else:
			return False

	@property
	def nombre_completo(self):
		return "{0} {1}".format(self.nombre, self.appellido)


class Clase(models.Model):
	nombre = models.CharField(max_length=250)
	nivel = models.ForeignKey(Nivel)
	descripcion = models.CharField(max_length=1000, blank=True, null=True)
	status = models.CharField(max_length=150, choices=(("A", "Activo"), ("I", "Inactivo")))

	def __unicode__(self):
		return u"%s %s" % (self.nombre, self.nivel)

	class Meta:
		ordering = ("nombre",)


class Clase_Profesor(models.Model):
	profesor = models.ForeignKey(Perfil_Profesor, null=True, blank=True)
	clase = models.ForeignKey(Clase, null=True, blank=True)

	def __unicode__(self):
		return u"%s - %s" % (self.profesor, self.clase)

	class Meta:
		verbose_name = "Profesor de Clase"
		verbose_name_plural = "Profesores de cada clase"


class Nota(models.Model):
	valor = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
	alumno = models.ForeignKey(Alumno)
	periodo = models.ForeignKey('Periodo')
	clase = models.ForeignKey(Clase)
	tipo = models.CharField(max_length=150)

	def __unicode__(self):
		return u"%s - %s" % (self.alumno, self.periodo)


class Periodo(models.Model):
	ano_lectivo = models.CharField(max_length=150, blank=True)
	quimestre = models.IntegerField(null=False)
	parcial = models.IntegerField(null=False)

	@property
	def nombre_periodo(self):
		_numero_string = {1: "primer", 2: "segundo", 3: "tercer"}
		n_parcial = _numero_string[self.parcial]
		n_quimestre = _numero_string[self.quimestre]
		return "%s parcial del %s quimestre %s" % (n_parcial, n_quimestre, self.ano_lectivo)

	@property
	def nombre_parcial(self):
		_nombres_parciales = {1: "Primer Parcial", 2: "Segundo Parcial", 3: "Tercer Parcial"}
		n_parcial = _nombres_parciales[self.parcial]
		return n_parcial

	def __unicode__(self):
		return self.nombre_periodo
