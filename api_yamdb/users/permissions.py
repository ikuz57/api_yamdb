from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

User = get_user_model()


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            raise AuthenticationFailed()
        username = request.user
        user = User.objects.get(username=username)
        return user.role == 'moderator'


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            raise AuthenticationFailed()
        username = request.user
        user = User.objects.get(username=username)
        return user.role == 'admin'


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class IsAuthorCreateAuthOrReadOnly(IsAuthorOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return permissions.IsAuthenticated
        else:
            return (super(IsAuthorCreateAuthOrReadOnly, self).
                    has_object_permission(request, view, obj))


class IsSuperuser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser
