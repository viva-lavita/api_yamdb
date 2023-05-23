from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

router = SimpleRouter()

router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    path(''),  # здесь будет аунтефикация
]
