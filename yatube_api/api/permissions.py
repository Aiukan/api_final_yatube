"""Разрешения для API проекта."""

from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    """Класс разрешения доступа редактирования для автора."""

    def has_permission(self, request, view):
        """Проверка авторизации для запросов на изменение данных."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """Проверка авторства для запросов на изменение данных."""
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
