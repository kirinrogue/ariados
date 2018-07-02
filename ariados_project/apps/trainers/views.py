from django.db import transaction
from django.db.models import Q
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from ariados.models import Trainer, FriendRequest, IsFriendOf
from .serializers import TrainerSerializer, TrainerUserSerializer, FriendRequestSerializer


# Create your views here.
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_trainer(request):
    id = request.GET.get('id', '')
    name = request.GET.get('name', '')
    try:
        if id:
            serializer = TrainerSerializer(Trainer.objects.get(id=id))
        else:
            serializer = TrainerSerializer(Trainer.objects.get(name=name))
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


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_friend_requests(request):
    try:
        trainer = Trainer.objects.get(user=request.user)
        frs = FriendRequest.objects.filter(trainer_to=trainer, status='SENT')
        serializer = FriendRequestSerializer(frs, many=True)
        # response = {'success': 'Friend request sent!'}
    except Exception as e:
        return Response({'error': str(e)})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def accept_friend_request_from(request):
    trainer_from_name = request.GET.get('trainer_name', '')
    try:
        with transaction.atomic():
            trainer = Trainer.objects.get(user=request.user)
            trainer_from = Trainer.objects.get(name=trainer_from_name)
            FriendRequest.objects.filter(trainer_to=trainer, trainer_from=trainer_from, status='SENT').update(
                status='ACCEPTED')
            IsFriendOf.objects.create(trainer1=trainer, trainer2=trainer_from)
        response = {'success': 'Friend request accepted!'}
    except Exception as e:
        return Response({'error': str(e)})
    return Response(response)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def reject_friend_request_from(request):
    trainer_from_name = request.GET.get('trainer_name', '')
    try:
        with transaction.atomic():
            trainer = Trainer.objects.get(user=request.user)
            trainer_from = Trainer.objects.get(name=trainer_from_name)
            FriendRequest.objects.filter(trainer_to=trainer, trainer_from=trainer_from, status='SENT').update(
                status='REJECTED')
        response = {'success': 'Friend request rejected!'}
    except Exception as e:
        return Response({'error': str(e)})
    return Response(response)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_friends(request):
    params = {}
    params.update(request.GET.items())
    try:
        trainer = Trainer.objects.get(user=request.user)
        friend_list = list(IsFriendOf.objects.filter(Q(trainer1=trainer) | Q(trainer2=trainer)).values_list('trainer1',
                                                                                                            flat=True))
        friend_list.extend(
            list(IsFriendOf.objects.filter(Q(trainer1=trainer) | Q(trainer2=trainer)).values_list('trainer2',
                                                                                                  flat=True)))
        if params:
            trainers = Trainer.objects.filter(id__in=friend_list, **params).exclude(id=trainer.id)
        else:
            trainers = Trainer.objects.filter(id__in=friend_list).exclude(id=trainer.id)
        serializer = TrainerSerializer(trainers, many=True)
    except Exception as e:
        return Response({'error': str(e)})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def update_location(request):
    lat = request.GET.get('lat', 0.0)
    lng = request.GET.get('lng', 0.0)
    try:
        Trainer.objects.filter(user=request.user).update(current_location='{0},{1}'.format(lat, lng))

        response = {'success': 'Updated!'}
    except Exception as e:
        return Response({'error': str(e)})
    return Response(response)
