from django.db import models

class Escuela(models.Model):
    cue = models.CharField(max_length=90, unique=True)
    dni = models.CharField(max_length=20)

    def __str__(self):
        return self.cue


class Alumno(models.Model):
    escuela = models.ForeignKey(
        Escuela,
        on_delete=models.CASCADE,
        related_name="alumnos"
    )

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)

    cumple_asistencia = models.BooleanField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"