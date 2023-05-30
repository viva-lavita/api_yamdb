from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from .filters import TitleFilters
from .permissions import AuthorOrStaffOrReadOnly, IsAdminOrReadOnly, IsAdmin
from .serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer,
    ReviewSerializer, TitleSerializer, TitleWriteSerializer,
    TokenSerializer, UserCreateSerializer, UsersSerializer
)
from reviews.models import Category, Genre, Review, Title
from users.models import User


class SignUpView(APIView):
    """
    POST-запрос с email и username генерирует
    письмо с кодом для получения токена.
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        """Создание пользователя И Отправка письма с кодом."""
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        user, code_created = User.objects.get_or_create(
            email=email, username=username)
        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        user.save()
        send_mail(
            subject='Код подтверждения',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=(user.email,),
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели User."""
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(detail=False, methods=['get', 'patch'], url_path='me',
            url_name='me', permission_classes=(permissions.IsAuthenticated,))
    def about_me(self, request):
        if request.method == 'PATCH':
            serializer = UserCreateSerializer(
                request.user, data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserCreateSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(APIView):
    """
    POST-запрос с username и confirmation_code
    возвращает JWT-токен.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if confirmation_code != user.confirmation_code:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        return Response({'token': str(refresh.access_token)},
                        status=status.HTTP_200_OK)


class CreateListDestroyViewSet(CreateModelMixin, DestroyModelMixin,
                               ListModelMixin, viewsets.GenericViewSet):
    """Кастом миксин вьюсет для моделей категорий и жанров."""
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]


class CategoryViewSet(CreateListDestroyViewSet):
    """Вьюсет для модели категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    """Вьюсет модели жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели произведений."""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilters
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TitleSerializer
        return TitleWriteSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrStaffOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrStaffOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serialaizer):
        serialaizer.save(
            title=get_object_or_404(
                Title,
                id=self.kwargs.get('title_id')
            ),
            author=self.request.user,
        )
