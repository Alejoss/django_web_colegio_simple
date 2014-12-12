from django.shortcuts import render


# Create your views here.
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


def sistema(request):
	template = "inicio/sistema.html"
	context = {}
	return render(request, template, context)
