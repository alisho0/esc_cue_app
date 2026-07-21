from django.urls import path

from .views import dashboard, escuelas, alumnos

app_name = 'panel'

urlpatterns = [
    path('', dashboard, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('escuelas/', escuelas, name='escuelas'),
    path('alumnos/', alumnos, name='alumnos'),
]
