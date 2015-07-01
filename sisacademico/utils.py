# -*- coding: utf-8 -*-
from sisacademico.models import Perfil_Profesor, Clase_Profesor, Matricula, \
                                Nota, Clase_Profesor, Clase


def obtener_perfil_profesor(user):
	perfil, creado = Perfil_Profesor.objects.get_or_create(usuario=user)
	return perfil


def obtener_clases_profesor(perfil_profesor):
	clases_profesor_obj = Clase_Profesor.objects.filter(profesor=perfil_profesor)
	clases = []
	for obj in clases_profesor_obj:
		clases.append(obj.clase)
	return clases


def obtener_alumnos_clase(clase):
	matriculas = Matricula.objects.filter(nivel=clase.nivel)
	alumnos = []
	for m in matriculas:
		alumnos.append(m.alumno)
	return alumnos


def obtener_editar_valor_nota(alumno, clase, periodo, tipo, valor=None):
	nota_obj, creado = Nota.objects.get_or_create(alumno=alumno, clase=clase,
		                                          periodo=periodo, tipo=tipo)
	if valor:
		nota_obj.valor = valor
		nota_obj.save()
	else:
		return nota_obj


def calcular_promedio_notas(notas):
	# Recibe diccionario con notas_objects.
	# Calcula el promedio_parcial y el promedio_final. El promedio parcial toma en cuenta notas no publicadas
	notas_promedio_parcial = []
	notas_promedio_final = []

	for nota in notas.itervalues():
		if nota.valor > 0:
			if not nota.publicada:
				notas_promedio_parcial.append(int(nota.valor))
			else:
				notas_promedio_parcial.append(int(nota.valor))
				notas_promedio_final.append(int(nota.valor))

	promedio_parcial = 0
	if len(notas_promedio_parcial) > 0:
		promedio_parcial = sum(notas_promedio_parcial)/float(len(notas_promedio_parcial))
		promedio_parcial = "%.2f" % promedio_parcial
	else:
		promedio_parcial = 0

	promedio_final = 0
	if len(notas_promedio_final) > 0:
		promedio_final = sum(notas_promedio_final)/float(len(notas_promedio_final))
		promedio_final = "%.2f" % promedio_final
	else:
		promedio_final = 0

	return promedio_parcial, promedio_final


def obtener_fila_alumno_notas(alumno, clase, periodo):
	# Para la vista del profesor
	notas = {}
	notas['tareas'] = obtener_editar_valor_nota(alumno, clase, periodo, "tareas")
	notas['actividades_individuales'] = obtener_editar_valor_nota(alumno, clase, periodo, "act_ind")
	notas['actividades_grupales'] = obtener_editar_valor_nota(alumno, clase, periodo, "act_gru")
	notas['lecciones'] = obtener_editar_valor_nota(alumno, clase, periodo, "lecciones")
	notas['pruebas'] = obtener_editar_valor_nota(alumno, clase, periodo, "pruebas")
	notas['promedios'] = calcular_promedio_notas(notas)	
	notas['alumno'] = alumno

	return notas


def obtener_clases_nivel(nivel):
	clases_nivel = Clase.objects.filter(nivel=nivel)
	return clases_nivel


def is_number(s):
	# prueba a ver si un string es un numero
	try:
		float(s)
		return True
	except (ValueError, TypeError):
		return False


def calcular_promedio_reporte_alumno(notas):
	# recibe el diccionario de obtener_notas_alumno
	notas_promedio = []
	for nota in notas.itervalues():
		if is_number(nota):
			notas_promedio.append(float(nota))

	promedio = "-"
	try:
		promedio = "{0:.2f}".format(sum(notas_promedio)/float(len(notas_promedio)))
	except ZeroDivisionError:
		promedio = "-"

	return promedio


def obtener_notas_alumno(alumno, clases, periodo):
	notas = []
	for clase in clases:
		notas_clase = {}
		notas_clase['clase'] = clase
		notas_obj = Nota.objects.filter(alumno=alumno, clase=clase, periodo=periodo, publicada=True)
		for nota in notas_obj:
			if nota.valor:
				notas_clase[nota.tipo] = nota.valor
			else:
				notas_clase[nota.tipo] = "-"

		notas_clase['promedio'] = calcular_promedio_reporte_alumno(notas_clase)

		notas.append(notas_clase)
	return notas
