from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        username = request.user
        user = User.objects.get(username=username)
        return user.role == 'moderator'

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        username = request.user
        user = User.objects.get(username=username)
        return user.role == 'moderator'


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        username = request.user
        user = User.objects.get(username=username)
        return user.role == 'admin'

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
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


class IsAuthorOrModerOrAdminCreateAuthOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                or IsModerator.has_permission(self, request, view)
                or IsAdmin.has_permission(self, request, view)
                or IsSuperuser.has_permission(self, request, view)
                )

    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return permissions.IsAuthenticated
        else:
            return (request.method in permissions.SAFE_METHODS
                    or obj.author == request.user
                    or IsModerator.has_object_permission(self, request, view,
                                                         obj)
                    or IsAdmin.has_object_permission(self, request, view, obj)
                    or IsSuperuser.has_object_permission(self, request, view,
                                                         obj)
                    )


class IsSuperuser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser
