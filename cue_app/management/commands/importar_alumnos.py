import csv
from datetime import datetime

from cue_app.models import Escuela, Alumno
from django.core.management.base import BaseCommand


def parse_fecha_nacimiento(valor):
    valor = (valor or '').strip()
    if not valor:
        return None

    for formato in ('%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%d/%m/%y'):
        try:
            return datetime.strptime(valor, formato).date()
        except ValueError:
            continue

    return None


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('archivo', type=str)

    def handle(self, *args, **kwargs):
        with open(kwargs['archivo'], newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                cue = (row.get('cue') or '').strip()

                if not cue:
                    self.stdout.write(self.style.WARNING('Se omite una fila sin CUE.'))
                    continue

                print("Buscando:", repr(cue))

                try:
                    escuela = Escuela.objects.get(cue=cue)
                except Escuela.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f'No se encontró la escuela con CUE {cue!r}. Se omite el alumno.')
                    )
                    continue

                cumple = None
                if 'cumple_asistencia' in row:
                    cumple = row['cumple_asistencia'].lower() == 'true'

                fecha_nacimiento = parse_fecha_nacimiento(row.get('nacimiento'))
                if row.get('nacimiento', '').strip() and fecha_nacimiento is None:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Fecha de nacimiento inválida {row['nacimiento']!r}. "
                            'Se carga el alumno sin fecha.'
                        )
                    )

                Alumno.objects.create(
                    escuela=escuela,
                    nombre=row['nombre'],
                    apellido=row['apellido'],
                    fecha_nacimiento=fecha_nacimiento,
                    cumple_asistencia=cumple,
                    curso=row['curso'],
                    localidad=row['localidad'],
                    dni=row['dni'],
                    creado_por_escuela=False,
                    editado_por_escuela=False
                )
            
            self.stdout.write(self.style.SUCCESS('Alumnos importados exitosamente'))