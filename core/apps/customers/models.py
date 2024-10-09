from uuid import uuid4
from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.customers.entities import CustomerEntity


class Customer(TimedBaseModel):
    phone = models.CharField(
        verbose_name='Номер телефона',
        max_length=20,
        unique=True,
        help_text='Уникальный номер телефона для каждого пользователя',
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
        return self.phone
    
    
    def to_entity(self) -> CustomerEntity:
        return CustomerEntity(
            phone=self.phone,
            created_at=self.created_at,
        )
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    
