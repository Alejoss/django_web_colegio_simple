# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm, TextInput

from sisacademico.models import Perfil_Profesor, Periodo, Nivel


class NumberInput(TextInput):
	input_type = 'number'


class FormBuscarAlumno(forms.Form):
	periodos_obj = Periodo.objects.all()
	periodos = []
	for p in periodos_obj:
		periodos.append((p.id, p.nombre_periodo))

	niveles_obj = Nivel.objects.all()
	niveles = []
	for n in niveles_obj:
		niveles.append((n.id, n.nombre))

	cedula = forms.IntegerField(required=False, widget=NumberInput(attrs={}))
	periodo = forms.ChoiceField(choices=periodos)
	nivel = forms.ChoiceField(choices=niveles)


class FormPerfilProfesor(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(FormPerfilProfesor, self).__init__(*args, **kwargs)
		self.fields['titulo'].required = False
		self.fields['num_contacto'].required = False

	class Meta:
		model = Perfil_Profesor
		fields = ('titulo', 'num_contacto')
		widgets = {
			'num_contacto': TextInput()
		}


class FormEditarNotas(forms.Form):

	tareas = forms.FloatField(required=False, max_value=10, min_value=0,
		widget=NumberInput(attrs={'id': 'form_tareas', 'step': '0.1'}))
	actividades_individuales = forms.DecimalField(required=False, max_value=10, min_value=0,
		widget=NumberInput(attrs={'id': 'form_act_ind', 'type': 'number', 'step': '0.1'}))
	actividades_grupales = forms.DecimalField(required=False, max_value=10, min_value=0,
		widget=NumberInput(attrs={'id': 'form_act_gru', 'type': 'number', 'step': '0.1'}))
	lecciones = forms.DecimalField(required=False, max_value=10, min_value=0,
		widget=NumberInput(attrs={'id': 'form_lecciones', 'type': 'number', 'step': '0.1'}))
	pruebas = forms.DecimalField(required=False, max_value=10, min_value=0,
		widget=NumberInput(attrs={'id': 'form_pruebas', 'type': 'number', 'step': '0.1'}))
	clase = forms.CharField(required=False,
		widget=TextInput(attrs={'id': 'form_clase'}))
	alumno = forms.CharField(required=False,
	    widget=TextInput(attrs={'id': 'form_alumno'}))
	periodo = forms.CharField(required=False,
		widget=TextInput(attrs={'id': 'form_periodo'}))
