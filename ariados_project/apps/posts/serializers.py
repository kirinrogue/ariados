from rest_framework import serializers

from apps.trainers.serializers import TrainerSerializer
from ariados.models import Trainer, Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'viewers', 'status', 'creator', 'answer_of', 'last_update')

    creator = TrainerSerializer(required=True)


class EditPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'viewers', 'status', 'answer_of', 'last_update')

    def save(self, request, validated_data):
        trainer = Trainer.objects.get(user=request.user)
        post, created = Post.objects.update_or_create(id=validated_data.pop('id'),
                                                      defaults={'trainer': trainer, **validated_data})
        return post
