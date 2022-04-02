from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        username = request.user
        user = User.objects.get(username=username)
        return user.role == 'moderator'
