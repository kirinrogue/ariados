from django.db import transaction
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from ariados import settings
from ariados.models import Trainer, FriendRequest, IsFriendOf, Post, Vote
from . import utiles
from .serializers import TrainerSerializer, PostSerializer, \
    EditPostSerializer


# Create your views here.
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_post(request):
    id = request.GET.get('id', '')
    try:
        serializer = PostSerializer(Post.objects.get(id=id))
    except Exception as e:
        return Response({'error': str(e)})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def filter_posts(request):
    try:
        params = {}
        params.update(request.GET.items())
        serializer = PostSerializer(Post.objects.filter(**params), many=True)
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
