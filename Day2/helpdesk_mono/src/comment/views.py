from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .permissions import IsOwner
from .serializers import CommentSerializer, CommentUpdateSerializer
from .models import Comment


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return CommentUpdateSerializer
        return super().get_serializer_class()
