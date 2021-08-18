from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import viewsets, filters, status
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import User
from .serializers import CustomUserSerializer, TokenSerializer, SignupSerializer
from .permissions import AdminOnly


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = "username"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("=username",)
    permission_classes = (AdminOnly,)

    @action(detail=False, methods=["GET", "PATCH"], permission_classes = (IsAuthenticated,))
    def me(self, request):
        if request.method == "PATCH":
            serializer = CustomUserSerializer(request.user, partial=True, data=request.data)
            if serializer.is_valid():
                serializer.validated_data.pop('role', False)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(username=request.user.username)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Signup(CreateAPIView):

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if not User.objects.filter(username=request.data["username"], email=request.data["email"]).exists():
                serializer.save()
            user = User.objects.get(username=request.data["username"], email=request.data["email"])
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                "Hello",
                f"Your confirmation Code - {confirmation_code}",
                "admin@yamdb.com",
                [serializer.data["email"]],
                fail_silently=True,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Token(CreateAPIView):

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(User, username=request.data["username"])
            confirmation_code = request.data["confirmation_code"]
            if default_token_generator.check_token(user, confirmation_code):
                token = AccessToken.for_user(user)
                response = {
                            "token": str(token)
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
