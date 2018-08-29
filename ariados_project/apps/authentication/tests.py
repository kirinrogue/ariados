# Create your tests here.
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from ariados.models import DjangoSession


class AuthenticationTestCase(TestCase):
    def setUp(self):
        # Creamos un usuario
        User.objects.create_user(username="test",
                                 email="test@email.com",
                                 password="test")

    def test_login_user(self):
        error = False
        try:
            # Nos logeamos para tener credenciales
            client = APIClient()
            client.login(username='test', password='test')
        except Exception:
            error = True

        self.assertTrue(not error)

    def test_logout_user(self):
        error = False
        try:
            client = APIClient()
            client.login(username='test', password='test')
            # llamamos a logout
            client.logout()
        except Exception:
            error = True

        self.assertTrue(not error)

    def test_get_session(self):
        client = APIClient()
        client.login(username='test', password='test')

        self.assertTrue(DjangoSession.objects.all().exists())

    def test_change_password(self):
        error = False
        try:
            # Nos logeamos para tener credenciales
            user = User.objects.get(username="test")
            user.set_password('new_pass')
            user.save()

            client = APIClient()
            client.login(username='test', password='new_pass')
        except Exception:
            error = True

        self.assertTrue(not error)
