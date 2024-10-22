from uuid import uuid4
from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.customers.entities import CustomerEntity


class Customer(TimedBaseModel):
    email = models.CharField(
        verbose_name='Почта пользователя',
        unique=True,
        help_text='Уникальный почта каждого пользователя',
    )

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=50,
        null=True,
    )

    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=50,
        null=True,
    )

    access_token = models.CharField(
        verbose_name='Токен авторизации',
        default=uuid4,
        max_length=255,
    )

    refresh_token = models.CharField(
        verbose_name='Токен для обновления access token',
        default=uuid4,
        max_length=255,
    )

    expires_in = models.BigIntegerField(
        verbose_name='Время до истечения access token',
        default=0,
    )

    refresh_expires_in = models.BigIntegerField(
        verbose_name='Время до истечения refresh token',
        default=0,
    )

    def __str__(self) -> str:
        return self.email

    def to_entity(self) -> CustomerEntity:
        return CustomerEntity(
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            created_at=self.created_at,
        )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
