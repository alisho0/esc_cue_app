from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from cue_app.models import Alumno, Escuela


class PanelAccessTests(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(
            username='admin_user',
            password='secret123',
            is_staff=True,
        )
        self.school_user = User.objects.create_user(
            username='school_user',
            password='secret123',
        )

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(reverse('panel:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('next=/panel/dashboard/', response.url)

    def test_non_admin_user_receives_forbidden(self):
        self.client.force_login(self.school_user)
        response = self.client.get(reverse('panel:dashboard'))
        self.assertEqual(response.status_code, 403)

    def test_staff_user_can_access_dashboard(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse('panel:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_panel/dashboard.html')

    def test_editing_alumno_without_checking_checkbox_keeps_assistance_false(self):
        escuela = Escuela.objects.create(nombre='Escuela Test', cue='123456')
        alumno = Alumno.objects.create(
            escuela=escuela,
            nombre='Juan',
            apellido='Pérez',
            curso='5to',
            dni='12345678',
            localidad='Ciudad',
            fecha_nacimiento='2008-01-01',
            cumple_asistencia=False,
        )

        self.client.force_login(self.staff_user)
        response = self.client.post(
            reverse('panel:alumno_editar', kwargs={'alumno_id': alumno.pk}),
            {
                'escuela': escuela.pk,
                'nombre': alumno.nombre,
                'apellido': alumno.apellido,
                'dni': alumno.dni,
                'curso': alumno.curso,
                'localidad': alumno.localidad,
                'fecha_nacimiento': '2008-01-01',
                'cumple_asistencia': 'off',
            },
        )

        self.assertEqual(response.status_code, 302)
        alumno.refresh_from_db()
        self.assertFalse(alumno.cumple_asistencia)
