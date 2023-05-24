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
        max_length=150,
        verbose_name='Логин',        
        unique=True,
        validators=([RegexValidator(regex=r'^[\w.@+-]+$')]))
    email = models.EmailField(max_length=254,
                              verbose_name='E-mail',                              
                              unique=True)
    confirmation_code = models.CharField(max_length=40,
                                         blank=True,
                                         null=True,
                                         verbose_name='Проверочный код')
    first_name = models.CharField(max_length=150,
                                  verbose_name='Имя',                                  
                                  blank=True)
    last_name = models.CharField(max_length=150,
                                 verbose_name='Фамилия',                                 
                                 blank=True)
    bio = models.TextField(max_length=1000,
                           verbose_name='Биография',                           
                           blank=True,)
    role = models.CharField(max_length=100,
                            verbose_name='Роль',
                            choices=USER_ROLE,
                            default=USER,
                            )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.is_staff or self.role == User.ADMIN

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR

    def __str__(self):
        return self.username
