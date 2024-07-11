from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Менеджер кастомной модели пользователя, где имя является уникальным идентификатором.
    """
    def create_user(self, name, password, **extra_fields):
        """
        Создает и возвращает пользователя с его именем и паролем
        """
        user = self.model(name=name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, password, **extra_fields):
        """Создает и возвращает админа с его именем и паролем"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(name, password, **extra_fields)