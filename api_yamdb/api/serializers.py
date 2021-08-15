from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, ValidationError

from users.models import User
from reviews.models import Categories, Genres, Titles


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Titles
        fields = '__all__'


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
