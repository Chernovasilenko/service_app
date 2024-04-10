from django.core.validators import MaxValueValidator
from django.db import models

from clients.models import Client


class Service(models.Model):
    """Сервис."""

    name = models.CharField(
        verbose_name='Название сервиса',
        max_length=50
        )
    full_price = models.PositiveIntegerField(verbose_name='Стоимость',)

    def __str__(self):
        return self.name


class Plan(models.Model):
    """Тарифный план."""

    PLAN_TYPES = (
        ('full', 'Full'),
        ('student', 'Students'),
        ('discount', 'Discount'),
    )

    plan_type = models.CharField(
        verbose_name='Тарифный план',
        choices=PLAN_TYPES,
        max_length=10
    )
    discount_percent = models.PositiveIntegerField(
        verbose_name='Процент скидки',
        default=0,
        validators=(MaxValueValidator(100),)
    )

    def __str__(self):
        return self.plan_type


class Subscription(models.Model):
    """Подписка."""

    client = models.ForeignKey(
        Client,
        verbose_name='Подписчик',
        related_name='subscriptions',
        on_delete=models.PROTECT
    )
    service = models.ForeignKey(
        Service,
        verbose_name='Сервис',
        related_name='subscriptions',
        on_delete=models.PROTECT
    )
    plan = models.ForeignKey(
        Plan,
        verbose_name='Сервис',
        related_name='subscriptions',
        on_delete=models.PROTECT
    )

    def __str__(self):
        return f'{self.client} подписан на {self.service}'
