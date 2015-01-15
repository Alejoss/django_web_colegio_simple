# -*- coding: utf-8 -*-
from sisacademico.models import Perfil_Profesor, Clase_Profesor, Matricula, Nota


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
		if creado:
			return 1
		else:
			return nota_obj.valor


def calcular_promedio_notas(notas):
	# Recibe diccionario con notas
	notas_promedio = []
	for value in notas.itervalues():
		if int(value) > 0:
			notas_promedio.append(int(value))
	if len(notas_promedio) > 0:
		promedio = sum(notas_promedio)/float(len(notas_promedio))
	else:
		promedio = 0
	return "%.2f" % promedio


def obtener_fila_alumno_notas(alumno, clase, periodo):
	notas = {}
	notas_obj = Nota.objects.filter(alumno=alumno, clase=clase, periodo=periodo)
	for nota in notas_obj:
		notas[nota.tipo] = nota.valor
	notas['tareas'] = obtener_editar_valor_nota(alumno, clase, periodo, "tareas")
	notas['actividades_individuales'] = obtener_editar_valor_nota(alumno, clase, periodo, "act_ind")
	notas['actividades_grupales'] = obtener_editar_valor_nota(alumno, clase, periodo, "act_gru")
	notas['lecciones'] = obtener_editar_valor_nota(alumno, clase, periodo, "lecciones")
	notas['pruebas'] = obtener_editar_valor_nota(alumno, clase, periodo, "pruebas")
	notas['promedio'] = calcular_promedio_notas(notas)
	notas['alumno'] = alumno

	return notas
