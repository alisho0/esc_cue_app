from django.contrib import admin
from .models import Alumno, Escuela

# Register your models here.
admin.site.register(Escuela)
admin.site.register(Alumno)
