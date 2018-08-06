from datetime import datetime

from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
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
    try:
        parent = Post.objects.get(title=title)
        posts = Post.objects.filter(answer_of=parent)
        serializer = PostSerializer(posts, many=True)
    except Exception as e:
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
@permission_classes((IsAuthenticated,))
def update_post(request):
    try:
        Post.objects.filter(title=request.POST.get('title', '')).update(text=request.POST.get('text', ''),
                                                                        last_update=datetime.now)
    except Exception as e:
        return Response({'error': str(e)})
    return Response({'success': 'Updated!'})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def save_post(request):
    try:
        parent = Post.object.get(title=request.POST.get('parent_title'))
        Post.objects.create(title=request.POST.get('title', ''), text=request.POST.get('text', ''), answer_of=parent,
                            status=parent.status, creator=Trainer.objects.get(user=request.user),
                            viewers=parent.viewers)
    except Exception as e:
        return Response({'error': str(e)})
    return Response({'success': 'Successfully answered!'})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def answer_post(request):
    try:
        serializer = EditPostSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        serializer.save(request=request, validated_data=serializer.validated_data)
    except Exception as e:
        return Response({'error': str(e)})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def delete_post(request):
    title = request.GET.get('title', '')
    try:
        Post.objects.filter(title=title).delete()
    except Exception as e:
        return Response({'error': str(e)})
    return Response({'success': 'Deleted successfully'})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def vote_post(request):
    post_title = request.GET.get('title', '')
    type = request.GET.get('type', '')
    try:
        trainer = Trainer.objects.get(user=request.user)
        post = Post.objects.get(title=post_title)
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
    post_title = request.GET.get('title', '')
    try:
        post = Post.objects.get(title=post_title)
        likes = Vote.objects.filter(post=post, type='LIKE')
        dislikes = Vote.objects.filter(post=post, type='DISLIKE')
        response = {'LIKES': likes.count(), 'DISLIKES': dislikes.count()}
    except Exception as e:
        return Response({'error': str(e)})
    return Response(response)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def is_author(request):
    post_title = request.GET.get('title', '')
    try:
        post = Post.objects.get(title=post_title)
        is_author = 1 if post.creator == Trainer.objects.get(user=request.user) else 0
        response = {'is_author': is_author}
    except Exception as e:
        return Response({'error': str(e)})
    return Response(response)
