"""Сериализаторы для API проекта."""
import base64

from rest_framework import serializers
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model

from posts.models import Post, Group, Comment, Follow


User = get_user_model()


class Base64ImageField(serializers.ImageField):
    """Поле для сохранения изображений в формате base64."""

    def to_internal_value(self, data):
        """Восстановление изображения из формата base64."""
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для класса Post."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        """Мета-информация сериализатора для класса Post."""

        model = Post
        fields = ('id', 'text', 'pub_date', 'author', 'image', 'group')


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для класса Group."""

    class Meta:
        """Мета-информация сериализатора для класса Group."""

        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для класса Comment."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        """Мета-информация сериализатора для класса Comment."""

        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для класса Follow."""

    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        """Meta-информация сериализатора для класса Follow."""

        model = Follow
        fields = ('id', 'user', 'following')
