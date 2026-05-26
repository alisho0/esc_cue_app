import csv

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from cue_app.models import Escuela


class Command(BaseCommand):

    def add_arguments(self, parser):

        parser.add_argument(
            'archivo',
            type=str
        )

    def handle(self, *args, **kwargs):

        with open(
            kwargs['archivo'],
            newline='',
            encoding='utf-8'
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                nombre = row['nombre']
                cue = row['cue']
                dni = row['dni']

                # Obtener o crear el usuario
                user, created = User.objects.get_or_create(
                    username=cue,
                    defaults={'password': dni}
                )

                # Obtener o crear la escuela
                escuela, created = Escuela.objects.get_or_create(
                    cue=cue,
                    defaults={
                        'user': user,
                        'nombre': nombre,
                        'dni': dni
                    }
                )

                # Si ya existía, actualizar los datos
                if not created:
                    escuela.nombre = nombre
                    escuela.dni = dni
                    escuela.user = user
                    escuela.save()

        self.stdout.write(
            self.style.SUCCESS(
                'Escuelas importadas correctamente'
            )
        )