from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    USER_ROLE = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )

    username = models.CharField(
        'Логин',
        max_length=150,
        unique=True,
        validators=([RegexValidator(regex=r'^[\w.@+-]+$')]))
    email = models.EmailField('E-mail',
                              max_length=254,
                              unique=True)
    confirmation_code = models.CharField('Проверочный код',
                                         max_length=40,
                                         blank=True,
                                         null=True)
    first_name = models.CharField('Имя',
                                  max_length=150,
                                  blank=True)
    last_name = models.CharField('Фамилия',
                                 max_length=150,
                                 blank=True)
    bio = models.TextField('Биография',
                           max_length=1000,
                           blank=True)
    role = models.CharField('Роль',
                            max_length=100,
                            choices=USER_ROLE,
                            default=USER)

    @property
    def is_admin(self):
        return self.is_staff or self.role == User.ADMIN

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR

    def __str__(self):
        return self.username
