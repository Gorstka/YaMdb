from rest_framework import viewsets
from rest_framework import pagination

from reviews.models import Titles, Genres, Categories
from .serializers import TitleSerializer, GenreSerializer, CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    pagination_class = pagination.LimitOffsetPagination


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer
    pagination_class = pagination.LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitleSerializer
    pagination_class = pagination.LimitOffsetPagination
