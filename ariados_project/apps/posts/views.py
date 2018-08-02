import re

import requests
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from ariados.models import Trainer, IsFriendOf, Post, Vote
from .serializers import PostSerializer, EditPostSerializer


# Create your views here.
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_post(request):
    id = request.GET.get('id', '')
    title = request.GET.get('title', '')
    try:
        if id:
            serializer = PostSerializer(Post.objects.get(id=id))
        else:
            serializer = PostSerializer(Post.objects.get(title=title))
    except Exception as e:
        return Response({'error': str(e)})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def filter_posts(request):
    try:
        trainer = Trainer.objects.get(user=request.user)
        team = trainer.team
        friend_list = list(IsFriendOf.objects.filter(Q(trainer1=trainer) | Q(trainer2=trainer)).values_list('trainer1',
                                                                                                            flat=True))
        friend_list.extend(
            list(IsFriendOf.objects.filter(Q(trainer1=trainer) | Q(trainer2=trainer)).values_list('trainer2',
                                                                                                  flat=True)))
        params = {}
        params.update(request.GET.items())
        posts = Post.objects.filter(Q(viewers=team) | Q(viewers='GLOBAL'), creator__id__in=friend_list,
                                    answer_of__isnull=True, **params)

        serializer = PostSerializer(posts, many=True)
    except Exception as e:
        return Response({'error': str(e)})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_answers(request):
    title = request.GET.get('title', '')
    print(title)
    try:
        parent = Post.objects.get(title=title)
        posts = Post.objects.filter(answer_of=parent)
        print(title, parent, posts)

        serializer = PostSerializer(posts, many=True)
    except Exception as e:
        print(e)
        return Response({'error': str(e)})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def filter_my_posts(request):
    try:
        trainer = Trainer.objects.get(user=request.user)
        params = {}
        params.update(request.GET.items())
        posts = Post.objects.filter(creator=trainer, **params)

        serializer = PostSerializer(posts, many=True)
    except Exception as e:
        return Response({'error': str(e)})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((AllowAny,))
def save_post(request):
    try:
        serializer = EditPostSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        serializer.save(request=request, validated_data=serializer.validated_data)
    except Exception as e:
        return Response({'error': str(e)})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def vote_post(request):
    post_id = request.GET.get('post_id', '')
    type = request.GET.get('type', '')
    try:
        trainer = Trainer.objects.get(user=request.user)
        post = Post.objects.get(id=post_id)
        if Vote.objects.filter(trainer=trainer, post=post).exists():
            Vote.objects.filter(trainer=trainer, post=post).update(type=type)
            response = {'error': 'Vote changed!'}
        else:
            Vote.objects.create(trainer=trainer, post=post, type=type)
            response = {'success': 'Voted!'}
    except Exception as e:
        return Response({'error': str(e)})
    return Response(response)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_votes(request):
    post_id = request.GET.get('post_id', '')
    try:
        post = Post.objects.get(id=post_id)
        likes = Vote.objects.filter(post=post, type='LIKE')
        dislikes = Vote.objects.filter(post=post, type='DISLIKE')
        response = {'LIKES': likes.count(), 'DISLIKES': dislikes.count()}
    except Exception as e:
        return Response({'error': str(e)})
    return Response(response)


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_pgo_events(request):
    # actualizaciones:
    # grid__item post-list__date-item : clase de los elementos fecha
    # grid__item post-list__title : clases de los elementos <a> que contienen el título


    # eventos:
    # events-list__event__date__day : clase para los días (span)
    # events-list__event__date__month : clase para el mes
    # events-list__event__content (CONTENIDO, DIVIDIO POR TITULO Y TEXTO)
    # events-list__event__title : clase para el título del evento
    # events-list__event__body : cuerpo / descripción del evento

    # renderizar template con jquery que imprimirá los valores que queremos,
    # y luego obtenerlos
    page = requests.get('https://pokemon.gameinfo.io/es/events').content.decode('utf-8')

    start = page.find('<section id="events">')
    end = page.find('</section>')
    content = page[start:end]

    string = render_to_string('events.html', context={'content': content})
    return HttpResponse(string)
