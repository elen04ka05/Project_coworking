from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User


class Workspace(models.Model):
    """Модель рабочего места"""
    name = models.CharField(
        max_length=255,
        verbose_name="Название"
    )
    location = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Локация"
    )
    capacity = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1)],
        verbose_name="Вместимость"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Рабочее место"
        verbose_name_plural = "Рабочие места"
        db_table = 'Workspace'
        ordering = ['-created_at']


class Reservation(models.Model):
    """Модель бронирования"""

    class Status(models.TextChoices):
        PENDING = 'pending', 'Ожидает'
        CONFIRMED = 'confirmed', 'Подтверждено'
        CANCELLED = 'cancelled', 'Отменено'
        COMPLETED = 'completed', 'Завершено'
        NO_SHOW = 'no_show', 'Неявка'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name="Пользователь"
    )
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name="Рабочее место"
    )
    reservation_date = models.DateField(
        verbose_name="Дата бронирования"
    )
    start_time = models.TimeField(
        verbose_name="Время начала"
    )
    duration_hours = models.IntegerField(
        verbose_name="Длительность (часы)",
        validators=[MinValueValidator(1), MaxValueValidator(24)]
    )
    status = models.CharField(
        max_length=50,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    def __str__(self):
        return f"Reservation #{self.id} - {self.user.email} - {self.workspace.name}"

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        db_table = 'Reservation'
        ordering = ['-reservation_date', 'start_time']
        # Уникальность: нельзя забронировать одно место в одно время
        unique_together = ['workspace', 'reservation_date', 'start_time']


class QRCode(models.Model):
    """Модель QR-кода"""
    reservation = models.OneToOneField(
        Reservation,
        on_delete=models.CASCADE,
        related_name='qr_code',
        verbose_name="Бронирование"
    )
    code_data = models.TextField(
        verbose_name="Данные QR-кода"
    )
    generated_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата генерации"
    )
    expires_at = models.DateTimeField(
        verbose_name="Дата истечения"
    )
    is_used = models.BooleanField(
        default=False,
        verbose_name="Использован"
    )

    def __str__(self):
        return f"QR for reservation #{self.reservation.id}"

    class Meta:
        verbose_name = "QR-код"
        verbose_name_plural = "QR-коды"
        db_table = 'QRCode'
        ordering = ['-generated_at']


class Report(models.Model):
    """Модель отчетов"""

    class ReportType(models.TextChoices):
        OCCUPANCY = 'occupancy', 'Заполняемость'
        USERS = 'users', 'Пользователи'
        WORKSPACES = 'workspaces', 'Рабочие места'

    generated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='generated_reports',
        verbose_name="Сгенерировал"
    )
    report_type = models.CharField(
        max_length=100,
        choices=ReportType.choices,
        verbose_name="Тип отчета"
    )
    period = models.CharField(
        max_length=50,
        verbose_name="Период"
    )
    data = models.JSONField(
        verbose_name="Данные отчета"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    def __str__(self):
        return f"{self.get_report_type_display()} - {self.period}"

    class Meta:
        verbose_name = "Отчет"
        verbose_name_plural = "Отчеты"
        db_table = 'Report'
        ordering = ['-created_at']