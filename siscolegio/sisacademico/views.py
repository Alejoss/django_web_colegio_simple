from django.contrib import auth
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from utils import obtener_perfil_profesor, obtener_clases_profesor, obtener_alumnos_clase,\
                obtener_fila_alumno_notas, obtener_editar_valor_nota
from models import Clase, Periodo, Perfil_Profesor, Alumno
from forms import FormPerfilProfesor, FormEditarNotas


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
	periodos_primer_quimestre = Periodo.objects.filter(quimestre=1)
	periodos_segundo_quimestre = Periodo.objects.filter(quimestre=2)
	context = {'periodos_primer_quimestre': periodos_primer_quimestre,
		       'periodos_segundo_quimestre': periodos_segundo_quimestre,
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


def logout(request):
    auth.logout(request)  # Logout el user guardado en Request
    return redirect('inicio:sislogin')
