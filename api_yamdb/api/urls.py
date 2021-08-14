from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, Signup, Token

router = DefaultRouter()

router.register("users", UserViewSet, basename = "users")

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/signup/", Signup.as_view()),
    path("v1/auth/token/", Token.as_view()),
    path("v1/auth/", include("djoser.urls")),
    path("v1/auth/", include("djoser.urls.jwt")),
]
