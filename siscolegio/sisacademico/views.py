# -*- coding: utf-8 -*-
from django.contrib import auth
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from easy_pdf.views import PDFTemplateView

from utils import obtener_perfil_profesor, obtener_clases_profesor, obtener_alumnos_clase,\
                obtener_fila_alumno_notas, obtener_editar_valor_nota, obtener_clases_nivel, \
                obtener_notas_alumno
from models import Clase, Periodo, Perfil_Profesor, Alumno, Nivel
from forms import FormPerfilProfesor, FormEditarNotas, FormBuscarAlumno


def authcheck(request):
	# standard auth de Django. Para usuarios especiales
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)
	if user is not None:
		auth.login(request, user)
		return redirect('sisacademico:clases')
	else:
		return redirect('inicio:sislogin')


def password_changed(request):
	template = 'sisacademico/password_changed.html'
	context = {}
	return render(request, template, context)


def perfil_profesor(request):
	template = "sisacademico/form_perfil_profesor.html"
	perfil_actual = get_object_or_404(Perfil_Profesor, usuario=request.user)
	if request.method == "POST":
		form = FormPerfilProfesor(request.POST, instance=perfil_actual)
		if form.is_valid():
			form.save()
			return redirect('sisacademico:perfil_profesor')
		else:
			return redirect('sisacademico:clases')
	else:
		form_editar_perfil = FormPerfilProfesor()
		context = {'form_editar_perfil': form_editar_perfil, 'perfil_actual': perfil_actual}

		return render(request, template, context)


@login_required
def clases(request):
	template = "sisacademico/lista_clases.html"
	perfil_profesor = obtener_perfil_profesor(request.user)
	clases_profesor = obtener_clases_profesor(perfil_profesor)
	context = {'clases_profesor': clases_profesor}
	return render(request, template, context)


@login_required
def clase_periodos(request, clase_id):
	template = "sisacademico/clase_periodos.html"
	clase = get_object_or_404(Clase, id=clase_id)
	periodos = Periodo.objects.all()
	context = {'periodos': periodos,
		       'clase': clase}
	return render(request, template, context)


# View con las Notas de cada alumno
@login_required
def clase_alumnos(request, clase_id, periodo_id):
	template = "sisacademico/clase.html"
	periodo = get_object_or_404(Periodo, id=periodo_id)
	clase = get_object_or_404(Clase, id=clase_id)
	alumnos_clase = obtener_alumnos_clase(clase)
	lista_datos = []
	for alumno in alumnos_clase:
		notas_alumno = obtener_fila_alumno_notas(alumno, clase, periodo)
		lista_datos.append(notas_alumno)
	form_editar_notas = FormEditarNotas
	context = {'clase': clase, 'periodo': periodo, 'lista_datos': lista_datos,
	           'form_editar_notas': form_editar_notas}

	return render(request, template, context)


@login_required
def editar_notas(request):
	if request.method == "POST":
		form = FormEditarNotas(request.POST)
		if form.is_valid():
			tareas = form.cleaned_data['tareas']
			actividades_individuales = form.cleaned_data['actividades_individuales']
			actividades_grupales = form.cleaned_data['actividades_grupales']
			pruebas = form.cleaned_data['pruebas']
			lecciones = form.cleaned_data['lecciones']

			clase = Clase.objects.get(pk=form.cleaned_data['clase'])
			alumno = Alumno.objects.get(pk=form.cleaned_data['alumno'])
			periodo = Periodo.objects.get(pk=form.cleaned_data['periodo'])

			obtener_editar_valor_nota(clase=clase, periodo=periodo, alumno=alumno, tipo="tareas", valor=tareas)
			obtener_editar_valor_nota(clase=clase, periodo=periodo, alumno=alumno, tipo="act_ind", valor=actividades_individuales)
			obtener_editar_valor_nota(clase=clase, periodo=periodo, alumno=alumno, tipo="act_gru", valor=actividades_grupales)
			obtener_editar_valor_nota(clase=clase, periodo=periodo, alumno=alumno, tipo="pruebas", valor=pruebas)
			obtener_editar_valor_nota(clase=clase, periodo=periodo, alumno=alumno, tipo="lecciones", valor=lecciones)

			return redirect('sisacademico:clase_alumnos', clase.id, periodo.id)


class ReporteNotasPDF(PDFTemplateView):

	def get_context_data(self, **kwargs):
		context = super(ReporteNotasPDF, self).get_context_data(**kwargs)
		periodo_id = kwargs["periodo_id"]
		clase_id = kwargs["clase_id"]
		periodo = get_object_or_404(Periodo, id=periodo_id)
		clase = get_object_or_404(Clase, id=clase_id)
		alumnos_clase = obtener_alumnos_clase(clase)
		lista_datos = []
		for alumno in alumnos_clase:
			notas_alumno = obtener_fila_alumno_notas(alumno, clase, periodo)
			lista_datos.append(notas_alumno)
		context["clase"] = clase
		context["periodo"] = periodo
		context["lista_datos"] = lista_datos
		return context

	template_name = "sisacademico/reporte_notas.html"


def logout(request):
    auth.logout(request)  # Logout el user guardado en Request
    return redirect('inicio:sislogin')


def alumnos(request):
	template = "sisacademico/alumnos.html"
	form_alumnos = FormBuscarAlumno
	context = {'form_alumnos': form_alumnos}
	return render(request, template, context)


def alumno_notas(request):
	template = "sisacademico/alumno_notas.html"

	nivel = get_object_or_404(Nivel, pk=request.GET["nivel"])
	alumno = get_object_or_404(Alumno, pk=request.GET["cedula"])
	periodo = get_object_or_404(Periodo, pk=request.GET["periodo"])

	clases = obtener_clases_nivel(nivel)
	notas = obtener_notas_alumno(alumno, clases, periodo)

	context = {'notas': notas, 'alumno': alumno, 'periodo': periodo}
	return render(request, template, context)
