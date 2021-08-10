from django.urls import path, include
from rest_framework import routers

from .views import TitleViewSet, CategoryViewSet, GenreViewSet

router = routers.DefaultRouter()
router.register(r'titles', TitleViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
]
