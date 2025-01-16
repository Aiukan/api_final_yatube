"""Разрешения для API проекта."""

from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    """Класс разрешения доступа редактирования для автора."""

    def has_object_permission(self, request, view, obj):
        """Функция проверки авторства для запросов на изменение и удаление."""
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.author == request.user
        return True
