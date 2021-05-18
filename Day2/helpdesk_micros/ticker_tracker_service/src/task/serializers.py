from rest_framework import serializers
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

    class Meta:
        model = Task
        fields = ('id', 'name', 'project', 'status', 'performer',
                  'author', 'description', 'comment')

    def perform_create(self, serializer):
        # The request user is set as author automatically.
        serializer.save(author=self.request.user)


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        fields = ('id', 'username', 'userstatus', 'token')