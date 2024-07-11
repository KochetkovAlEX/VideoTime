from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Модель кастомного пользователя"""
    name = models.CharField(max_length=50, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.name


class Video(models.Model):
    """Модель видеороликов"""
    title = models.CharField(max_length=30)
    video = models.FileField(null=True, validators=[FileExtensionValidator(['mp4'])])
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    likes = models.JSONField(default=dict, blank=True)


class Post(models.Model):
    """Модель постов(комментариев)"""
    post = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, blank=True, null=True)
