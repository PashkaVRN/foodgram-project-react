from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission

User = get_user_model()


class IsAdminOrReadOnly(BasePermission):
    """
    Пользователь является супрюзером джанго
    или имеет роль администратора.
    Просмотр доступен всем пользователям.
    """
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (request.user.is_authenticated
                and request.user.is_admin)
        )


class IsAuthorModeratorAdminOrReadOnly(BasePermission):
    """
    Пользователь является супрюзером джанго
    или имеет роль администратора или модератора.
    Просмотр доступен всем пользователям.
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)
