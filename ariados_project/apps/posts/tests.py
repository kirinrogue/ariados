from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from ariados.models import Post, Trainer


class PostTestCase(TestCase):
    def setUp(self):
        # Creamos un usuario
        user = User.objects.create_user(username="test",
                                        email="test@email.com",
                                        password="test")
        trainer = Trainer.objects.create(name="trainer_test", team='VALOR', home_location='Seville',
                                         current_location='0 0', user=user)
        # Creamos el evento previo para usarlo en el resto de tests
        Post.objects.create(title="Join me in the next raid!",
                            text="Lorem ipsum dolor sit amet.",
                            viewers="GLOBAL", creator=trainer, status="OPEN", answer_of=None)

    def test_create_post(self):
        post = Post.objects.get(title="Join me in the next raid!")
        self.assertEqual(post.viewers, 'GLOBAL')

    def test_filter_post(self):
        posts = Post.objects.filter(title__contains="raid")
        self.assertTrue(posts.exists())

    def test_auth_get_answers(self):
        post = Post.objects.get(title="Join me in the next raid!")

        client = APIClient()
        client.login(username='test', password='test')
        response = client.get('/posts/answers/?title=' + post.title)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_post(self):
        Post.objects.filter(title="Join me in the next raid!").update(status='CLOSED')
        post = Post.objects.get(title="Join me in the next raid!")

        self.assertEqual(post.status, 'CLOSED')

    def test_auth_get_votes(self):
        post = Post.objects.get(title="Join me in the next raid!")

        client = APIClient()
        client.login(username='test', password='test')
        response = client.get('/posts/votes/?title=' + post.title)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anon_get_answers(self):
        post = Post.objects.get(title="Join me in the next raid!")

        client = APIClient()
        response = client.get('/posts/answer/?title=' + post.title)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
