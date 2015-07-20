# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import password_change
# from forms import FormCambiarPassword

from sisacademico import views

urlpatterns = patterns('',
		url(r'^alumno_notas/$', views.reporte_alumno_notas, name='alumno_notas'),
		url(r'^reporte_quimestre/$', views.reporte_quimestre, name='reporte_quimestre'),
		url(r'^reporte_matricula/$', views.reporte_matricula, name='reporte_matricula'),
		url(r'^alumnos/(?P<tipo_reporte>\w+)/$', views.alumnos, name='alumnos'),

		url(r'^authcheck/$', views.authcheck, name='authcheck'),
		url(r'^cambiar_password/password_changed/$', views.password_changed, name='password_changed'),
		url(r'^cambiar_password/$', password_change,
			{'template_name': 'sisacademico/cambiar_password.html',
			 'post_change_redirect': 'password_changed/',
			 'password_change_form': PasswordChangeForm},
			    name='cambiar_password'),

		url(r'^perfil_profesor/$', views.perfil_profesor, name='perfil_profesor'),
		url(r'^logout/$', views.logout, name='logout'),
		url(r'^clases/$', views.clases, name='clases'),
		url(r'^clase/(?P<clase_id>\d+)/(?P<periodo_id>\d+)/$', views.clase_alumnos, name='clase_alumnos'),
		url(r'^clase/(?P<clase_id>\d+)/$', views.clase_periodos, name='clase_periodos'),
		url(r'^editar_notas/$', views.editar_notas, name='editar_notas'),

		url(r'^matricular_grupo/$', views.matricular_grupo, name='matricular_grupo'),
		url(r'^publicar_nota/$', views.publicar_nota, name='publicar_nota'),
		url(r'^esconder_nota/$', views.esconder_nota, name='esconder_nota'),
	)
