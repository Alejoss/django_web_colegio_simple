# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from sisacademico import views

urlpatterns = patterns('',
		url(r'^authcheck/$', views.authcheck, name='authcheck'),
		url(r'^perfil_profesor/$', views.perfil_profesor, name='perfil_profesor'),
		url(r'^logout/$', views.logout, name='logout'),
		url(r'^clases/$', views.clases, name='clases'),
		url(r'^clase/(?P<clase_id>\d+)/(?P<periodo_id>\d+)/$', views.clase_alumnos, name='clase_alumnos'),
		url(r'^clase/(?P<clase_id>\d+)/$', views.clase_periodos, name='clase_periodos'),
		url(r'^editar_notas/$', views.editar_notas, name='editar_notas'),
		url(r'^reporte_notas/(?P<clase_id>\d+)/(?P<periodo_id>\d+)/$', views.ReporteNotasPDF.as_view(), name='reporte_notas')
	)
