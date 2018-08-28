from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from ariados.models import Event


class EventTestCase(TestCase):
    def setUp(self):
        # Creamos un usuario
        User.objects.create_user(username="test",
                                 email="test@email.com",
                                 password="test")
        # Creamos el evento previo para usarlo en el resto de tests
        Event.objects.create(title="Community Day: Eevee!",
                             description="Lorem ipsum dolor sit amet.",
                             days="17-18 AUG")

    def test_create_event(self):
        eevee = Event.objects.get(title="Community Day: Eevee!")
        self.assertEqual(eevee.days, '17-18 AUG')

    def test_filter_event(self):
        events = Event.objects.filter(title__contains="Community")
        self.assertTrue(events.exists())

    def test_events_scraper(self):
        # Test para comprobar el correcto funcionamiento del web scraper que se ejecuta periódicamente
        client = APIClient()
        response = client.get('/events/update/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_auth_get_events(self):
        # Nos logeamos para tener credenciales
        client = APIClient()
        client.login(username='test', password='test')
        # llamamos a la funcionalidad /events/ de la api para obtener los eventos almacenados con el scrapper
        response = client.get('/events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anon_get_events(self):
        client = APIClient()
        response = client.get('/events/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
