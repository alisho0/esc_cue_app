import os
import tempfile

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from .forms import AlumnoForm
from .models import Alumno, Escuela


class AlumnoFormTests(TestCase):
    def test_form_includes_fecha_nacimiento_field(self):
        form = AlumnoForm()

        self.assertIn('fecha_nacimiento', form.fields)


class LoginTests(TestCase):
    def test_superuser_can_login_without_school(self):
        User = get_user_model()
        user = User.objects.create_user(username='admin', password='secret123', is_superuser=True, is_staff=True)

        response = self.client.post('/', {'cue': 'admin', 'dni': 'secret123'})

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('/panel/dashboard/'))
        self.assertTrue(user.is_authenticated)


class ImportarAlumnosTests(TestCase):
    def test_importa_alumno_con_fecha_nacimiento_vacia(self):
        Escuela.objects.create(nombre='Escuela Test', cue='1234')

        with tempfile.NamedTemporaryFile('w', suffix='.csv', delete=False, encoding='utf-8') as archivo:
            archivo.write('cue,nombre,apellido,nacimiento,curso,localidad,dni\n1234,Juan,Perez,   ,5A,Localidad,12345\n')
            ruta = archivo.name

        try:
            call_command('importar_alumnos', ruta)
        finally:
            os.remove(ruta)

        alumno = Alumno.objects.get(dni='12345')
        self.assertIsNone(alumno.fecha_nacimiento)

    def test_ignora_alumnos_cuando_la_escuela_no_existe(self):
        with tempfile.NamedTemporaryFile('w', suffix='.csv', delete=False, encoding='utf-8') as archivo:
            archivo.write('cue,nombre,apellido,nacimiento,curso,localidad,dni\n9999,Juan,Perez,2000-01-01,5A,Localidad,12345\n')
            ruta = archivo.name

        try:
            call_command('importar_alumnos', ruta)
        finally:
            os.remove(ruta)

        self.assertEqual(Alumno.objects.count(), 0)
