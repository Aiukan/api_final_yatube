"""Сериализаторы для API проекта."""

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model

from posts.models import Post, Group, Comment, Follow


User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для класса Post."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    image = serializers.ImageField(required=False, allow_null=True)

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
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        """Meta-информация сериализатора для класса Follow."""

        model = Follow
        fields = ('user', 'following')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            )
        ]

    def validate_following(self, value):
        """Проверка невозможности подписки на самого себя."""
        request = self.context.get('request')
        if (value == request.user):
            raise ValidationError('Подписка на самого себя запрещена.')
        return value
