from rest_framework import (
    permissions, viewsets, pagination, generics, filters, status)
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import ModelMultipleChoiceFilter, FilterSet, CharFilter
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import action
from rest_framework.response import Response

from reviews.models import Titles, Genres, Categories
from .serializers import (
    TitleSerializer, GenreSerializer,
    CategorySerializer, CustomUserSerializer,
    TokenSerializer, SignupSerializer)
from users.models import User
from .permissions import AdminOnly, IsAdminOrReadOnly


class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    pagination_class = pagination.PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)


class CategoryDestroy(generics.DestroyAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = ('slug')


class GenreListCreate(generics.ListCreateAPIView):
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer
    pagination_class = pagination.PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)


class GenreDestroy(generics.DestroyAPIView):
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = ('slug')


class ModelFilter(FilterSet):
    genre = ModelMultipleChoiceFilter(
        field_name='genre__slug',
        queryset=Genres.objects.all(),
        to_field_name='slug')
    category = ModelMultipleChoiceFilter(
        field_name='category__slug',
        queryset=Categories.objects.all(),
        to_field_name='slug')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    year = ModelMultipleChoiceFilter(
        field_name='year',
        queryset=Titles.objects.all(),
        to_field_name='year')

    class Meta:
        model = Titles
        fields = {
            'genre': ['exact'],
            'category': ['exact'],
            'name': ['contains'],
            'year': ['exact']}


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ModelFilter
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = "username"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("=username",)
    permission_classes = (AdminOnly,)

    @action(
        detail=False,
        methods=["GET", "PATCH"],
        permission_classes=(permissions.IsAuthenticated,))
    def me(self, request):
        if request.method == "PATCH":
            serializer = CustomUserSerializer(
                request.user, partial=True, data=request.data)
            if serializer.is_valid():
                serializer.validated_data.pop('role', False)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(username=request.user.username)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Signup(generics.CreateAPIView):

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if not User.objects.filter(username=request.data["username"],
                                       email=request.data["email"]).exists():
                serializer.save()
            user = User.objects.get(
                username=request.data["username"], email=request.data["email"])
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


class Token(generics.CreateAPIView):

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
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
