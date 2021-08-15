from django.urls import path, include
from rest_framework import routers

from .views import (
    TitleViewSet, CategoryList, CategoryDelete, GenreList, GenreDelete)

router = routers.DefaultRouter()
router.register(r'titles', TitleViewSet)


urlpatterns = [
    path('v1/categories/', CategoryList.as_view()),
    path('v1/categories/<slug:slug>', CategoryDelete.as_view()),
    path('v1/genres/', GenreList.as_view()),
    path('v1/genres/<slug:slug>', GenreDelete.as_view()),
    path('v1/', include(router.urls)),
]
