from openpyxl import Workbook

from .models import Alumno, Escuela


def generar_excel_global():

    wb = Workbook()

    ws = wb.active

    ws.title = "Alumnos"

    headers = [
        "Escuela",
        "CUE",
        "Nombre",
        "Apellido",
        "Curso",
        "Cumple el 80% de asistencia"
    ]

    ws.append(headers)

    alumnos = Alumno.objects.select_related(
        'escuela'
    )

    for alumno in alumnos:

        ws.append([
            alumno.escuela.nombre,
            alumno.escuela.cue,
            alumno.nombre,
            alumno.apellido,
            alumno.curso,
            "Sí" if alumno.cumple_asistencia else "No"
        ])

    return wb


def generar_excel_escuela(escuela_id):

    wb = Workbook()

    ws = wb.active

    try:
        escuela = Escuela.objects.get(id=escuela_id)
        ws.title = escuela.cue[:31]  # Excel limita nombres a 31 caracteres
    except Escuela.DoesNotExist:
        ws.title = "Alumnos"

    headers = [
        "Nombre",
        "Apellido",
        "Cumple el 80% de asistencia"
    ]

    ws.append(headers)

    alumnos = Alumno.objects.filter(
        escuela_id=escuela_id
    )

    for alumno in alumnos:

        ws.append([
            alumno.nombre,
            alumno.apellido,
            "Sí" if alumno.cumple_asistencia else "No"
        ])

    return wb