from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Модель кастомного пользователя"""
    name = models.CharField(max_length=50, unique=True, verbose_name='Имя пользователя')
    is_staff = models.BooleanField(default=False, verbose_name='Сотрудник')
    is_active = models.BooleanField(default=True, verbose_name='Активность')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Дата создания аккаунта')

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.name


class Video(models.Model):
    """Модель видеороликов"""
    title = models.CharField(max_length=30, verbose_name='Название видео')
    video_url = models.URLField(null=True, max_length=500, verbose_name='Ссылка на облако')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'видео'
        verbose_name_plural = 'Видео'

    def __str__(self):
        return self.title


class Comments(models.Model):
    """Модель постов(комментариев)"""
    text = models.CharField(max_length=255, null=True, verbose_name='Текст комментария')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Ссылка на видео')

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text


class Likes(models.Model):
    """Модель лайков"""
    video = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name='Понравившееся видео')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')


    class Meta:
        verbose_name = 'лайк'
        verbose_name_plural = 'Лайки'

    def __str__(self):
        return f'{self.user} -> {self.video}'