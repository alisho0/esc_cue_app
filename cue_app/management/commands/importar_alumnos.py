import csv
from escuelas.models import Escuela, Alumno
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('archivo', type=str)

    def handle(self, *args, **kwargs):
        with open(kwargs['archivo'], newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                escuela = Escuela.objects.get(cue=row['cue'])

                Alumno.objects.create(
                    escuela=escuela,
                    nombre=row['nombre'],
                    apellido=row['apellido']
                )