from django.contrib import admin
from django.shortcuts import redirect

from sisacademico.models import Alumno, Matricula, Nivel, Perfil_Profesor, Clase, \
                                Clase_Profesor, Periodo


def matricular_grupo(modelAdmin, request, queryset):
	selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)

	request.session['cedulas'] = selected

	return redirect('sisacademico:matricular_grupo')

matricular_grupo.short_description = "Matricular en Grupo"


class AlumnoAdmin(admin.ModelAdmin):

	actions = [matricular_grupo]


admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Matricula)
admin.site.register(Nivel)
admin.site.register(Perfil_Profesor)
admin.site.register(Clase)
admin.site.register(Clase_Profesor)
admin.site.register(Periodo)
