import csv
from cue_app.models import Escuela
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('archivo', type=str)

    def handle(self, *args, **kwargs):
        with open(kwargs['archivo'], newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                Escuela.objects.create(
                    cue=row['cue'],
                    dni=row['dni']
                )