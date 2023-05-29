from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, SignUpView, TitleViewSet,
                    TokenView, UsersViewSet)


app_name = 'api'

router_v1 = SimpleRouter()

router_v1.register('users', UsersViewSet, basename='users')
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitleViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include([
        path('signup/', SignUpView.as_view()),
        path('token/', TokenView.as_view())
    ])),
]
