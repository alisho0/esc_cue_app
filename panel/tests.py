from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


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
