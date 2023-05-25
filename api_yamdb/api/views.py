# from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from reviews.models import Review, Title
from .serializers import CommentSerializer, ReviewSerializer
from .permissions import AuthorOrStaffOrReadOnly


class CategoryViewSet(viewsets.ViewSet):
    pass


class GenreViewSet(viewsets.ViewSet):
    pass


class TitleViewSet(viewsets.ViewSet):
    pass


class CommentViewSet(viewsets.ViewSet):
    """Вьюсет для комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrStaffOrReadOnly,)

    def get_queryset(self):
        """Переопределяем метод queryset."""
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )
        return review.comments_review.all()

    def perform_create(self, serializer):
        """Переопределяем метод create."""
        serializer.save(
            review=get_object_or_404(
                Review,
                id=self.kwargs.get('review_id'),
                title__id=self.kwargs.get('title_id')
            ),
            author=self.request.user
        )


class ReviewViewSet(viewsets.ViewSet):
    """Вьюсет для отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrStaffOrReadOnly,)

    def get_queryset(self):
        """Переопределяем метод queryset."""
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )
        return review.reviews_title.all()

    def perform_create(self, serialaizer):
        """Переопределяем метод create."""
        serialaizer.save(
            tittle=get_object_or_404(
                Title,
                id=self.kwargs.get('title_id')
            ),
            author=self.request.user,
        )
