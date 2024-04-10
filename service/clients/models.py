from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Client(models.Model):
    """Клиент."""

    user = models.OneToOneField(
        User,
        verbose_name='Пользователь',
        on_delete=models.PROTECT
        )
    company_name = models.CharField(
        verbose_name='Компания',
        max_length=100
        )
    full_adress = models.CharField(
        verbose_name='Адрес',
        max_length=100
        )

    def __str__(self) -> str:
        return self.user.username
