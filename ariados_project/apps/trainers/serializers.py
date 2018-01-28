from django.contrib.auth.models import User
from rest_framework import serializers

from apps.authentication.serializers import UserSerializer
from ariados.models import Trainer


class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = ('name', 'team', 'home_location', 'current_location', 'user')

    user = UserSerializer(required=True)


class TrainerUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Trainer
        fields = ('name', 'team', 'home_location', 'current_location', 'user')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        trainer = Trainer.objects.create(user=user, **validated_data)
        return trainer
