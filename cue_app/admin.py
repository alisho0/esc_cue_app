from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Escuela, Alumno

# Register your models here.

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):

    list_display = (
        'apellido',
        'nombre',
        'escuela',
        'cumple_asistencia',
        'creado_por_escuela'
    )

    list_filter = (
        'creado_por_escuela',
        'cumple_asistencia'
    )
@admin.register(Escuela)
class EscuelaAdmin(admin.ModelAdmin):

    change_list_template = (
        'admin/escuelas_change_list.html'
    )

    list_display = (
        'nombre',
        'cue',
        'asistencia_completada',
        'exportar_excel'
    )

    list_filter = (
        'asistencia_completada',
    )

    def exportar_excel(self, obj):

        url = reverse(
            'exportar_escuela',
            args=[obj.id]
        )

        return format_html(
            '<a class="button" '
            'href="{}">'
            'Descargar Excel'
            '</a>',
            url
        )

    exportar_excel.short_description = 'Excel'