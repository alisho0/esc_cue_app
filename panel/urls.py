from django.urls import path

from .views import dashboard, escuelas, alumnos, alumno_crear, alumno_editar, alumno_eliminar

app_name = 'panel'

urlpatterns = [
    path('', dashboard, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('escuelas/', escuelas, name='escuelas'),
    path('alumnos/', alumnos, name='alumnos'),
    path('alumnos/nuevo/', alumno_crear, name='alumno_crear'),
    path('alumnos/<int:alumno_id>/editar/', alumno_editar, name='alumno_editar'),
    path('alumnos/<int:alumno_id>/eliminar/', alumno_eliminar, name='alumno_eliminar'),
]
