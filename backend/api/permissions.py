from rest_framework.permissions import SAFE_METHODS, BasePermission


class AuthorPermission(BasePermission):
    """Делаем так, чтобы изменять и добавлять объекты
       мог только их автор"""

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user)
