from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views import CommentViewSet, ReviewViewSet

router = DefaultRouter()
router.register('comments', CommentViewSet)
router.register('reviews', ReviewViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]