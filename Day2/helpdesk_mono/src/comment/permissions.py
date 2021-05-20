from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.author != request.user:
            return request.method in permissions.SAFE_METHODS
        return super().has_object_permission(request, view, obj)