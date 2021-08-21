from rest_framework import (
    permissions, viewsets, pagination, generics, filters, status, mixins)
from django_filters.rest_framework import DjangoFilterBackend
from api_yamdb import settings

from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.validators import ValidationError

from reviews.pagination import ReviewsPagination, CommentsPagination
from reviews.models import Title, Genre, Category, Review, Comment
from .serializers import (
    TitleReadSerializer, TitleWriteSerializer, GenreSerializer,
    CategorySerializer, CustomUserSerializer,
    TokenSerializer, SignupSerializer, ReviewSerializer, CommentSerializer)
from users.models import User
from .permissions import (
    AdminOnly, IsAdminOrReadOnly,
    IsAuthorOrAdminOrModerator)
from .filters import ModelFilter


class CreateDestroyListViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin,
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    pass


class CategoryViewSet(CreateDestroyListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    pagination_class = pagination.PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(CreateDestroyListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    pagination_class = pagination.PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleWriteSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ModelFilter
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitleWriteSerializer


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
            if not serializer.is_valid():
                raise ValidationError(serializer.errors)
            serializer.validated_data.pop('role', False)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Signup(generics.CreateAPIView):

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        if not User.objects.filter(username=serializer.validated_data["username"],
                                       email=serializer.validated_data["email"]).exists():
            serializer.save()
        user = get_object_or_404(User, 
            username=serializer.validated_data["username"], email=serializer.validated_data["email"])
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            "Hello",
            f"Your confirmation Code - {confirmation_code}",
            settings.EMAIL_HOST_USER,
            [serializer.validated_data["email"]],
            fail_silently=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class Token(generics.CreateAPIView):

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        user = get_object_or_404(User, username=serializer.validated_data["username"])
        confirmation_code = serializer.validated_data["confirmation_code"]
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            response = {
                "token": str(token)
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrModerator,)
    pagination_class = CommentsPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        comments = review.comments.all()
        return comments

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = ReviewsPagination
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrAdminOrModerator
    )

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        reviews = title.reviews.all()
        return reviews

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
        int_rating = Review.objects.filter(title=title).aggregate(Avg('score'))
        title.rating = int_rating['score__avg']
        title.save(update_fields=["rating"])

    def perform_update(self, serializer):
        serializer.save()
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        int_rating = Review.objects.filter(title=title).aggregate(Avg('score'))
        title.rating = int_rating['score__avg']
        title.save(update_fields=["rating"])
