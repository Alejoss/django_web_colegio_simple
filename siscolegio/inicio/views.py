# -*- coding: utf-8 -*-
from django.shortcuts import render


def sislogin(request):
	template = "inicio/sislogin.html"
	context = {}
	return render(request, template, context)


def inicio(request):
	template = "inicio/inicio.html"
	context = {}
	return render(request, template, context)


def colegio(request):
	template = "inicio/colegio.html"
	context = {}
	return render(request, template, context)


def docentes(request):
	template = "inicio/docentes.html"
	context = {}
	return render(request, template, context)


def estudiantes(request):
	template = "inicio/estudiantes.html"
	context = {}
	return render(request, template, context)


def blog(request):
	template = "inicio/blog.html"
	context = {}
	return render(request, template, context)
