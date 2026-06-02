from django.db import models
from django.contrib.auth.models import User

class Escuela(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='escuela',
        null=True,
        blank=True
    )

    nombre = models.CharField(max_length=150)

    cue = models.CharField(
        max_length=50,
        unique=True
    )

    dni = models.CharField(
        max_length=20,
        blank=True
    )

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
    curso = models.CharField(max_length=150)
    dni = models.CharField(max_length=150)
    localidad = models.CharField(max_length=150)

    cumple_asistencia = models.BooleanField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"