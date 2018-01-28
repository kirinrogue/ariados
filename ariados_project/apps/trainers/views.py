from rest_framework.decorators import api_view
from rest_framework.response import Response

from ariados.models import Trainer
from .serializers import TrainerSerializer


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
