from django.urls import path
from .views import *

urlpatterns = [
    path('', login_view, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('exportar/', exportar_excel, name='exportar_excel'),
    path('exportar/<int:escuela_id>/', exportar_escuela, name='exportar_escuela'),
    path('finalizar-carga/', finalizar_carga, name='finalizar_carga')
]