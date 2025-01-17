"""Представления для API проекта."""

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model

from posts.models import Post, Group, Comment, Follow
from .serializers import (
    PostSerializer, GroupSerializer, CommentSerializer, FollowSerializer
)
from .permissions import AuthorOrReadOnly


User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Post."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AuthorOrReadOnly,)

    def perform_create(self, serializer):
        """Переопределение метода perform_create для PostViewSet.

        Автоматическое добавление автора поста.
        """
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет модели Group."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = tuple()


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Comment."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        """Переопределение метода get_queryset для CommentViewSet.

        Извлекает информацию о посте из аргументов
        и возвращает связанные комментарии.
        """
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return post.comments.all()

    def perform_create(self, serializer):
        """Переопределение метода perform_create для PostViewSet.

        Автоматическое добавление номера поста и автора поста к комментарию.
        """
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        serializer.save(
            author=self.request.user,
            post=post
        )


class FollowViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Вьюсет для модели Follow."""

    serializer_class = FollowSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """Фильтрация несвязанных объектов для GET запроса."""
        user = self.request.user
        return Follow.objects.filter(user=user)

    def perform_create(self, serializer):
        """Добавление в сериализатор информации о пользователе."""
        if (serializer.validated_data['following'] == self.request.user):
            raise ValidationError('Подписка на самого себя запрещена.')
        if self.get_queryset().filter(
            following=serializer.validated_data['following']
        ).exists():
            raise ValidationError('Подписка на пользователя уже выполнена.')
        serializer.save(user=self.request.user)
