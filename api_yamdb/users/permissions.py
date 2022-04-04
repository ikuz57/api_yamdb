from django.contrib.auth import get_user_model
from rest_framework import permissions
from .models import MODERATOR, ADMIN

User = get_user_model()


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        username = request.user
        return request.user.role == MODERATOR

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        username = request.user
        return request.user.role == MODERATOR


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        username = request.user
        return request.user.role == ADMIN

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        username = request.user
        return request.user.role == ADMIN


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class IsSuperuser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser
