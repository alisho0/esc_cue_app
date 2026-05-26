import csv
from cue_app.models import Escuela, Alumno
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('archivo', type=str)

    def handle(self, *args, **kwargs):
        with open(kwargs['archivo'], newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                escuela = Escuela.objects.get(cue=row['cue'])

                cumple = None
                if 'cumple_asistencia' in row:
                    cumple = row['cumple_asistencia'].lower() == 'true'

                Alumno.objects.create(
                    escuela=escuela,
                    nombre=row['nombre'],
                    apellido=row['apellido'],
                    cumple_asistencia=cumple,
                    curso=row['curso']
                )
            
            self.stdout.write(self.style.SUCCESS('Alumnos importados exitosamente'))