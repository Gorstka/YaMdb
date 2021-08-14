from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import viewsets, filters, status
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from users.models import User
from .serializers import CustomUserSerializer, TokenSerializer, SignupSerializer
from .permissions import IsAdminOnly


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = "username"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("=username",)
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=["get", "patch"], permission_classes = (IsAuthenticated,))
    def me(self, request):
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
                f"Confirmation Code - {confirmation_code}",
                "admin@yamdb.com",
                serializer.data["email"],
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
                response = {"username": request.data["username"],
                            "token": str(token)
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
