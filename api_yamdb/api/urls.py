from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet, Signup, Token
from .views import (
    TitleViewSet, CategoryList, CategoryDelete, GenreList, GenreDelete)

router = routers.DefaultRouter()
router.register(r'titles', TitleViewSet)
router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path('v1/categories/', CategoryList.as_view()),
    path('v1/categories/<slug:slug>', CategoryDelete.as_view()),
    path('v1/genres/', GenreList.as_view()),
    path('v1/genres/<slug:slug>', GenreDelete.as_view()),
    path('v1/', include(router.urls)),
]

urlpatterns += [
    path("v1/", include(router.urls)),
    path("v1/auth/signup/", Signup.as_view()),
    path("v1/auth/token/", Token.as_view()),
    path("v1/auth/", include("djoser.urls")),
    path("v1/auth/", include("djoser.urls.jwt")),
]
