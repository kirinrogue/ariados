from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from ariados.models import Trainer, FriendRequest
from .serializers import TrainerSerializer, TrainerUserSerializer


# Create your views here.
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_trainer(request, id):
    try:
        if id:
            serializer = TrainerSerializer(Trainer.objects.get(id=id))
        else:
            serializer = TrainerSerializer(Trainer.objects.get(name=request.GET.get('name', '')))
    except Exception as e:
        return Response({'error': str(e)})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def filter_trainers(request):
    try:
        params = {}
        params.update(request.GET.items())
        serializer = TrainerSerializer(Trainer.objects.filter(**params), many=True)
    except Exception as e:
        return Response({'error': str(e)})
    return Response(serializer.data)


def show_test(request):
    serializer = TrainerUserSerializer()
    return render(request, 'trainer_test.html', {'serializer': serializer})


@api_view(['POST'])
@permission_classes((AllowAny,))
def save_trainer(request):
    try:
        serializer = TrainerUserSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    except Exception as e:
        return Response({'error': str(e)})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def send_friend_request(request):
    trainer_name = request.GET.get('trainer_name', '')
    try:
        trainer = Trainer.objects.get(user=request.user)
        trainer_to = Trainer.objects.get(name=trainer_name)
        if FriendRequest.objects.filter(trainer_from=trainer, trainer_to=trainer_to).exists():
            status = FriendRequest.objects.get(trainer_from=trainer, trainer_to=trainer_to).status
            response = {'error': 'Your friend request has already been {0}.'.format(status.lower())}
        else:
            FriendRequest.objects.create(trainer_from=trainer, trainer_to=trainer_to, status='SENT')
            response = {'success': 'Friend request sent!'}
    except Exception as e:
        return Response({'error': str(e)})
    return Response(response)
