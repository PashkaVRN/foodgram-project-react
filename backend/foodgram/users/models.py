from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator


class User(AbstractUser):
    """ Модель пользователя. """
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name', 'email', )
    first_name = models.CharField(
        verbose_name='Имя',
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
    )
    email = models.EmailField(
        verbose_name='email',
        unique=True
    )
    username = models.CharField(
        verbose_name='username',
        unique=True,
        validators=(UnicodeUsernameValidator(), )
    )

    class Meta:
        ordering = ('username', )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    """ Модель подписки на автора. """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='following'
    )
