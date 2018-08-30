from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from ariados.models import Trainer


class TrainerTestCase(TestCase):
    def setUp(self):
        # Creamos un usuario
        user = User.objects.create_user(username="test",
                                        email="test@email.com",
                                        password="test")
        user2 = User.objects.create_user(username="test2",
                                         email="test2@email.com",
                                         password="test2")
        trainer = Trainer.objects.create(name="trainer_test", team='VALOR', home_location='Seville',
                                         current_location='', user=user)
        trainer2 = Trainer.objects.create(name="trainer_test2", team='INSTINCT', home_location='Utrera',
                                          current_location='', user=user2)

    def test_create_trainer(self):
        t = Trainer.objects.get(name="trainer_test2")
        self.assertEqual(t.team, 'INSTINCT')

    def test_filter_trainer(self):
        posts = Trainer.objects.filter(name__contains="test")
        self.assertTrue(posts.exists())

    def test_auth_get_requests(self):
        client = APIClient()
        client.login(username='test', password='test')
        response = client.get('/trainers/get_friend_requests/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_location(self):
        client = APIClient()
        client.login(username='test', password='test')
        response = client.get('/trainers/update_location/?lat={0}&lng={1}'.format(37.155979, -5.924085))
        t = Trainer.objects.get(user=User.objects.get(username="test"))

        self.assertEqual(str(t.current_location), '37.155979,-5.924085')

    def test_auth_send_request(self):
        t = Trainer.objects.get(name="trainer_test2")

        client = APIClient()
        client.login(username='test', password='test')
        response = client.get('/trainers/send_friend_request/?trainer_name=' + t.name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_auth_get_closest(self):
        client = APIClient()
        client.login(username='test', password='test')
        response = client.get('/trainers/get_closest_trainers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anon_get_closest(self):
        client = APIClient()
        response = client.get('/trainers/get_closest_trainers/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
