from rest_framework import serializers

from apps.authentication.serializers import UserSerializer
from ariados.models import Trainer


class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = ('name', 'team', 'home_location', 'current_location', 'user')

    user = UserSerializer(required=True)
