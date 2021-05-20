from rest_framework import serializers

from comment.serializers import CommentSerializer
from .models import Task, Description


class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = ('id', 'task', 'text')

    def update(self, instance, validated_data):
        validated_data.pop('task')
        return super().update(instance, validated_data)


class TaskSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.id')
    description = DescriptionSerializer(many=True, read_only=True)
    comment = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'name', 'project', 'status', 'performer',
                  'author', 'description', 'comment')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
