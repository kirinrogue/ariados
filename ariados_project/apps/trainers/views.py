from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ariados.models import Trainer
from .serializers import TrainerSerializer, TrainerUserSerializer

from apps.authentication.serializers import UserSerializer


# Create your views here.
@api_view(['GET'])
def get_trainer(request, id):
    try:
        serializer = TrainerSerializer(Trainer.objects.get(id=id))
    except Exception as e:
        return Response({'error': str(e)})
    return Response(serializer.data)


@api_view(['GET'])
def filter_trainers(request):
    try:
        params = request.GET
        serializer = TrainerSerializer(Trainer.objects.filter(**params), many=True)
    except Exception as e:
        return Response({'error': str(e)})
    return Response(serializer.data)


def show_test(request):
    serializer = TrainerUserSerializer()
    return render(request, 'trainer_test.html', {'serializer': serializer})


@api_view(['POST'])
def save_trainer(request):
    try:
        serializer = TrainerUserSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    except Exception as e:
        return Response({'error': str(e)})
    return Response(serializer.data)
