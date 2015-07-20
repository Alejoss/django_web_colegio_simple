# -*- coding: utf-8 -*-
from django.contrib import auth
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from utils import obtener_perfil_profesor, obtener_clases_profesor, obtener_alumnos_clase,\
                obtener_fila_alumno_notas, obtener_editar_valor_nota, obtener_clases_nivel, \
                obtener_notas_alumno, obtener_notas_quimestre
from models import Clase, Periodo, Perfil_Profesor, Alumno, Nivel, Matricula, Nota
from forms import FormPerfilProfesor, FormEditarNotas, FormReportePeriodo, FormMatricularGrupo, FormReporteQuimestre


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


def logout(request):
    auth.logout(request)  # Logout el user guardado en Request
    return redirect('inicio:sislogin')


def matricular_grupo(request):
	template = "sisacademico/matricular_grupo.html"

	cedulas = request.session['cedulas']
	alumnos = []

	if request.method == "POST":
		form = FormMatricularGrupo(request.POST)

		if form.is_valid():
			ano_lectivo = form.cleaned_data["ano_lectivo"]
			nivel_id = form.cleaned_data["nivel"]
			
			nivel_obj = Nivel.objects.get(id=nivel_id)
			matriculas_creadas = []

			for c in cedulas:
				try:
					alumnos.append(Alumno.objects.get(cedula=c))
				except:
					pass

			for a in alumnos:
				if Matricula.objects.filter(nivel=nivel_obj, ano_lectivo=ano_lectivo, alumno=a).exists():
					print "matricula de alumno %s ya existe" % (a.nombre)
				else:
					nueva_matricula = Matricula(nivel=nivel_obj, ano_lectivo=ano_lectivo, alumno=a)
					nueva_matricula.save()
					matriculas_creadas.append(nueva_matricula)

			template = "sisacademico/matriculas_creadas.html"
			context = {'matriculas_creadas': matriculas_creadas}

			return render(request, template, context)
		
		else:

			return HttpResponse("no valid")

	else:
		form = FormMatricularGrupo()

	for c in cedulas:
		try:
			alumnos.append(Alumno.objects.get(cedula=c))
		except:
			pass

	context = {'alumnos': alumnos, 'form': form}

	return render(request, template, context)


def publicar_nota(request):

	nota_id = request.GET.get("id", '')	

	if nota_id:
		nota = Nota.objects.get(id=nota_id)
		nota.publicada = True
		nota.save()
		return HttpResponse('Nota marcada como publica')
	else:
		return HttpResponse(status_code=500)


def esconder_nota(request):

	nota_id = request.GET.get("id", '')

	if nota_id:
		nota = Nota.objects.get(id=nota_id)
		nota.publicada = False
		nota.save()
		return HttpResponse('No marcada como no publica')
	else:
		return HttpResponse(status_code=500)


def alumnos(request, tipo_reporte):
	template = "sisacademico/alumnos.html"

	if tipo_reporte == "quimestral":
		form = FormReporteQuimestre
	else:
		form = FormReportePeriodo
	context = {'form': form, 'tipo': tipo_reporte}
	return render(request, template, context)


def reporte_alumno_notas(request):
	template = "sisacademico/alumno_notas.html"

	alumno = get_object_or_404(Alumno, pk=request.GET.get("cedula", " "))
	nivel = get_object_or_404(Nivel, pk=request.GET.get("nivel", ""))
	periodo = get_object_or_404(Periodo, pk=request.GET.get("periodo", ""))
	clases = obtener_clases_nivel(nivel)
	notas = obtener_notas_alumno(alumno, clases, periodo)
	context = {'nivel': nivel, 'alumno': alumno, 'periodo': periodo, 'clases': clases, 'notas': notas}

	return render(request, template, context)


def reporte_quimestre(request):
	template = "sisacademico/reporte_quimestral.html"
	
	nivel = get_object_or_404(Nivel, pk=request.GET.get("nivel", ""))
	alumno = get_object_or_404(Alumno, pk=request.GET.get("cedula", ""))
	ano = request.GET.get("ano", "")
	quimestre = request.GET.get("quimestre", "")

	periodos = Periodo.objects.filter(ano_lectivo=ano, quimestre=quimestre)
	clases = obtener_clases_nivel(nivel)
	
	notas = obtener_notas_quimestre(alumno, clases, periodos)	

	context = {'nivel': nivel, 'alumno': alumno, 'quimestre': quimestre, 'clases': clases, 'notas': notas, 'ano': ano}

	return render(request, template, context)


def reporte_matricula(request):
	template = "sisacademico/reporte_matricula.html"

	ids_matriculas = request.session['matriculas']	

	matriculas = []
	for id_matricula in ids_matriculas:
		matricula_obj = get_object_or_404(Matricula, id=id_matricula)
		matriculas.append(matricula_obj)

	context = {'matriculas': matriculas}
	
	return render(request, template, context)
