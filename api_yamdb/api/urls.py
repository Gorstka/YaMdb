from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet, Signup, Token
from .views import (
    TitleViewSet, GenreListCreate, GenreDestroy,
    CategoryListCreate, CategoryDestroy,
    ReviewViewSet, CommentViewSet)

router = routers.DefaultRouter()
router.register('titles', TitleViewSet)
router.register('users', UserViewSet, basename='users')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)


urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/categories/", CategoryListCreate.as_view()),
    path("v1/categories/<slug:slug>/", CategoryDestroy.as_view()),
    path("v1/genres/", GenreListCreate.as_view()),
    path("v1/genres/<slug:slug>/", GenreDestroy.as_view()),
    path("v1/auth/signup/", Signup.as_view()),
    path("v1/auth/token/", Token.as_view()),
    path("v1/auth/", include("djoser.urls")),
    path("v1/auth/", include("djoser.urls.jwt")),
]
