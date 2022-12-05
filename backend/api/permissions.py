from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class AuthorPermission(permissions.BasePermission):
    """Делаем так, чтобы изменять и добавлять объекты
       мог только их автор"""

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


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
