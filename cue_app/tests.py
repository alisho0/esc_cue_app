from django.test import TestCase

from .forms import AlumnoForm


class AlumnoFormTests(TestCase):
    def test_form_includes_fecha_nacimiento_field(self):
        form = AlumnoForm()

        self.assertIn('fecha_nacimiento', form.fields)
