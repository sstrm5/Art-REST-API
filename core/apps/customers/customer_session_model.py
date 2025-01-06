import time
from uuid import uuid4
from django.db import models
from core.apps.customers.models import Customer
from core.apps.customers.entities import CustomerSession as CustomerSessionEntity
from core.apps.common.models import TimedBaseModel


class CustomerSession(TimedBaseModel):
    def get_expires_in():
        return int(time.time()) + 3600

    def get_refresh_expires_in():
        return int(time.time()) + 1209600

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

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
        default=get_expires_in,
    )

    refresh_expires_in = models.BigIntegerField(
        verbose_name='Время до истечения refresh token',
        default=get_refresh_expires_in,
    )
    device_info = models.CharField(max_length=255, blank=True, null=True)

    def to_entiity(self) -> CustomerSessionEntity:
        return CustomerSessionEntity(
            id=self.id,
            customer=self.customer.to_entity(),
            access_token=self.access_token,
            refresh_token=self.refresh_token,
            expires_in=self.expires_in,
            refresh_expires_in=self.refresh_expires_in,
            device_info=self.device_info,
        )

    def __str__(self):
        return f'Session - {self.customer.email} - {self.device_info}'

    class Meta:
        verbose_name = 'Сессия пользователя'
        verbose_name_plural = 'Сессии пользователей'
