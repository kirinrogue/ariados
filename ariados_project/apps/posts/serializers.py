from rest_framework import serializers

from ariados.models import Trainer, Post


class PostSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source='creator.name')

    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'viewers', 'status', 'creator_name', 'answer_of', 'last_update')


class EditPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'viewers', 'status', 'answer_of', 'last_update')

    def save(self, request, validated_data):
        trainer = Trainer.objects.get(user=request.user)
        post, created = Post.objects.update_or_create(id=validated_data.pop('id'),
                                                      defaults={'trainer': trainer, **validated_data})
        return post
