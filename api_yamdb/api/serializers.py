from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, ValidationError

from users.models import User
from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
        slug_field = ('slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        slug_field = ('slug')


class Genre_CategoryField(serializers.SlugRelatedField):
    def __init__(self, **kwargs):
        self.model_serializer_class = kwargs.pop('serializer')
        super().__init__(**kwargs)

    def to_representation(self, value):
        return self.model_serializer_class(instance=value).data


class TitleSerializer(serializers.ModelSerializer):
    genre = Genre_CategoryField(
        queryset=Genre.objects.all(), serializer=GenreSerializer, many=True,
        slug_field='slug')
    category = Genre_CategoryField(
        queryset=Category.objects.all(), serializer=CategorySerializer,
        slug_field='slug')

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category')


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            "username", "email", "role", "bio", "first_name", "last_name")
        model = User
        extra_kwargs = {"email": {"required": True}}
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=("email",),
                message="Почта уже существует",
            )
        ]


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("username",)
        model = User


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("email", "username")
        model = User
        extra_kwargs = {"email": {"required": True}}
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=("email",),
                message="Почта уже существует",
            )
        ]

    def validate_username(self, value):
        if value == "me":
            raise ValidationError(
                "Нельзя регистрировать имя пользователя 'me'")
        return value
