from django.core.validators import MaxValueValidator
from django.db import models

from clients.models import Client
from services.tasks import set_comment, set_price


class Service(models.Model):
    """Сервис."""

    name = models.CharField(
        verbose_name='Название сервиса',
        max_length=50
        )
    full_price = models.PositiveIntegerField(verbose_name='Стоимость',)

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__full_price = self.full_price

    def __str__(self):
        return self.name

    def save(self,  *args, **kwargs):
        if self.full_price != self.__full_price:
            for subscription in self.subscriptions.all():
                set_price.delay(subscription.id)
                set_comment.delay(subscription.id)
        return super().save(*args, **kwargs)


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

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__discount_percent = self.discount_percent

    def __str__(self):
        return self.plan_type

    def save(self,  *args, **kwargs):
        if self.discount_percent != self.__discount_percent:
            for subscription in self.subscriptions.all():
                set_price.delay(subscription.id)
                set_comment.delay(subscription.id)
        return super().save(*args, **kwargs)


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
    price = models.PositiveIntegerField(
        verbose_name='Стоимость',
        default=0,
    )
    comment = models.CharField(
        verbose_name='Комментарий',
        max_length=50,
        default='',
    )

    def __str__(self):
        return f'{self.client} подписан на {self.service}'
