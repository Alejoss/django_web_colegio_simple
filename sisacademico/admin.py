from django.contrib import admin
from sisacademico.models import Alumno, Matricula, Nivel, Perfil_Profesor, Clase, \
                                Clase_Profesor, Periodo

# Register your models here.
admin.site.register(Alumno)
admin.site.register(Matricula)
admin.site.register(Nivel)
admin.site.register(Perfil_Profesor)
admin.site.register(Clase)
admin.site.register(Clase_Profesor)
admin.site.register(Periodo)
