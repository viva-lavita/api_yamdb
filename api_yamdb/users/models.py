from django.contrib.auth.models import AbstractUser
from django.db import models


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
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        max_length=40,
        choices=CHOICE_ROLES,
        default='user',
        blank=True
    )

    def __str__(self) -> str:
        return self.username
