from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import SignUpView, TokenView, UsersViewSet

app_name = 'users'


v1_router = SimpleRouter()

v1_router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/', include([
        path('signup/', SignUpView.as_view()),
        path('token/', TokenView.as_view())
    ])),
]
