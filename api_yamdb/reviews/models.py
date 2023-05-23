from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


CHOICE_ROLES = [
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Админ')
]


class User(AbstractUser):
    """Кастом юзер."""
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    # по умолчанию есть у модели, не знаю, есть ли смысл дублировать
    # first_name = models.CharField(max_length=150, blank=True)
    # last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        max_length=40,
        choices=CHOICE_ROLES,
        default='user',
        blank=True
    )

    def __str__(self) -> str:
        return self.username


class Category(models.Model):
    """Категории (типы) произведений."""
    name = models.CharField('Категория', max_length=256)
    slug = models.SlugField(unique=True)  # null и blank по умолчанию False

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    """Жанры."""
    name = models.CharField('Жанр', max_length=256)
    slug = models.SlugField(unique=True)  # null и blank по умолчанию False

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    """Произведения."""
    name = models.CharField('Назвение произведения', max_length=256)
    year = models.IntegerField('Год выпуска')
    description = models.TextField('Описание', null=True, blank=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    """Отзывы."""
    text = models.CharField(max_length=200)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='reviews'
    )
    score = models.ImageField(
        'Оценка',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='reviews'
    )

    def __str__(self) -> str:
        return self.text

    class Meta:
        unique_together = ('title', 'author')
        ordering = ('pub_date',)


class Comment(models.Model):
    """Комментарии."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField('Текст комментария')
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self) -> str:
        return self.text

    class Meta:
        ordering = ('pub_date',)
