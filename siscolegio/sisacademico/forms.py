from django import forms
from django.forms import ModelForm, TextInput, NumberInput

from sisacademico.models import Perfil_Profesor


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

	tareas = forms.IntegerField(required=False, widget=NumberInput(attrs={'id': 'form_tareas'}))
	actividades_individuales = forms.IntegerField(required=False, widget=NumberInput(attrs={'id': 'form_act_ind'}))
	actividades_grupales = forms.IntegerField(required=False, widget=NumberInput(attrs={'id': 'form_act_gru'}))
	lecciones = forms.IntegerField(required=False, widget=NumberInput(attrs={'id': 'form_lecciones'}))
	pruebas = forms.IntegerField(required=False, widget=NumberInput(attrs={'id': 'form_pruebas'}))
	clase = forms.CharField(required=False, widget=TextInput(attrs={'id': 'form_clase'}))
	alumno = forms.CharField(required=False, widget=TextInput(attrs={'id': 'form_alumno'}))
	periodo = forms.CharField(required=False, widget=TextInput(attrs={'id': 'form_periodo'}))
