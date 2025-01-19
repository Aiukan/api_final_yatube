"""Представления для API проекта."""

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django.contrib.auth import get_user_model

from posts.models import Post, Group, Comment
from .serializers import (
    PostSerializer, GroupSerializer, CommentSerializer, FollowSerializer
)
from .permissions import IsAuthorOrReadOnly


User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Post."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        """Переопределение метода perform_create для PostViewSet.

        Автоматическое добавление автора поста.
        """
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет модели Group."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (AllowAny,)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Comment."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def get_post(self):
        """Возвращение поста по полученным аргументам."""
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def get_queryset(self):
        """Возвращает связанные комментарии для найденного поста."""
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        """Автоматическое добавление номера и автора поста к комментарию."""
        post = self.get_post()
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
        """Извлечение связанных подписок для GET запроса."""
        return self.request.user.followers.all()

    def perform_create(self, serializer):
        """Добавление в сериализатор информации о пользователе."""
        serializer.save(user=self.request.user)
