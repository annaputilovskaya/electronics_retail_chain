from rest_framework.permissions import BasePermission


class IsActiveUser(BasePermission):
    """
    Проверяет, активен ли пользователь.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active
