from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet, Signup, Token
from .views import (
    TitleViewSet, GenreViewSet, CategoryViewSet,
    ReviewViewSet, CommentViewSet)

router = routers.DefaultRouter()
router.register('titles', TitleViewSet)
router.register('users', UserViewSet, basename='users')
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
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
    path("", include(router.urls)),
    path("auth/signup/", Signup.as_view(), name='signup'),
    path("auth/token/", Token.as_view(), name='token'),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
