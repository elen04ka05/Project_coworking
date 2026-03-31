# core/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.postgres.fields import ArrayField


class UserManager(BaseUserManager):
    """Менеджер для кастомной модели пользователя"""

    def create_user(self, email, full_name, password=None, **extra_fields):
        """
        Создание обычного пользователя
        """
        if not email:
            raise ValueError('Email обязателен')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            full_name=full_name,
            **extra_fields
        )
        user.set_password(password)  # Хешируем пароль
        user.save(using=self._db)

        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        """
        Создание суперпользователя (администратора)
        """
        # Устанавливаем права суперпользователя
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # Проверяем, что права установлены корректно
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True')

        return self.create_user(email, full_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Кастомная модель пользователя
    Использует email как уникальный идентификатор вместо username
    """
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name="Email",
        db_index=True
    )
    full_name = models.CharField(
        max_length=255,
        verbose_name="Полное имя"
    )
    phone_number = models.CharField(
        max_length=58,
        blank=True,
        null=True,
        verbose_name="Номер телефона"
    )

    # Поля для Django auth
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен"
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="Персонал"
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name="Суперпользователь"
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата регистрации"
    )
    last_login = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Последний вход"
    )

    # Поле для входа (вместо username используем email)
    USERNAME_FIELD = 'email'

    # Обязательные поля при создании суперпользователя
    REQUIRED_FIELDS = ['full_name']

    # Подключаем менеджер
    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        db_table = 'User'
        ordering = ['-date_joined']


class Visitor(models.Model):
    """Модель посетителя (связь 1:1 с пользователем)"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='visitor_profile',
        verbose_name="Пользователь"
    )
    favorite_workspaces = ArrayField(
        models.BigIntegerField(),
        blank=True,
        default=list,
        verbose_name="Избранные рабочие места"
    )

    def __str__(self):
        return f"Visitor: {self.user.email}"

    class Meta:
        verbose_name = "Посетитель"
        verbose_name_plural = "Посетители"
        db_table = 'Visitor'


class Administrator(models.Model):
    """Модель администратора"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='admin_profile',
        verbose_name="Пользователь"
    )
    managed_locations = ArrayField(
        models.BigIntegerField(),
        blank=True,
        default=list,
        verbose_name="Управляемые локации"
    )

    def __str__(self):
        return f"Admin: {self.user.email}"

    class Meta:
        verbose_name = "Администратор"
        verbose_name_plural = "Администраторы"
        db_table = 'Administrator'