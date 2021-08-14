from djoser.serializers import UserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


from users.models import User

class CustomUserSerializer(UserSerializer):
    
    class Meta:
        fields = ("id", "username", "email", "role", "bio", "first_name", "last_name")
        model = User


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("username",)
        model = User


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ["email", "username"]
        model = User
