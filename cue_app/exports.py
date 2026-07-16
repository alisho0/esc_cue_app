from openpyxl import Workbook

from .models import Alumno, Escuela


def generar_excel_global():

    wb = Workbook()

    ws = wb.active

    ws.title = "Alumnos"

    headers = [
        "Nombre",
        "Apellido",
        "DNI",
        "Fecha de Nacimiento",
        "Localidad",
        "Curso",
        "Escuela",
        "CUE",
        "Cumple el 80% de asistencia",
        "Creado por escuela",
        "Editado por escuela"
    ]

    ws.append(headers)

    alumnos = Alumno.objects.select_related(
        'escuela'
    )

    for alumno in alumnos:
        ws.append([
            alumno.nombre,
            alumno.apellido,
            alumno.dni,
            alumno.fecha_nacimiento,
            alumno.localidad,
            alumno.curso,
            alumno.escuela.nombre,
            alumno.escuela.cue,
            "Sí" if alumno.cumple_asistencia else "No",
            "Sí" if alumno.creado_por_escuela else "No",
            "Sí" if alumno.editado_por_escuela else "No",
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
        "DNI",
        "Fecha de Nacimiento",
        "Localidad",
        "Curso",
        "Escuela",
        "CUE",
        "Cumple el 80% de asistencia",
        "Creado por escuela",
        "Editado por escuela"
    ]

    ws.append(headers)

    alumnos = Alumno.objects.filter(
        escuela_id=escuela_id
    )

    for alumno in alumnos:

        ws.append([
            alumno.nombre,
            alumno.apellido,
            alumno.dni,
            alumno.fecha_nacimiento,
            alumno.localidad,
            alumno.curso,
            alumno.escuela.nombre,
            alumno.escuela.cue,
            "Sí" if alumno.cumple_asistencia else "No",
            "Sí" if alumno.creado_por_escuela else "No"
            "Sí" if alumno.editado_por_escuela else "No"
        ])

    return wb