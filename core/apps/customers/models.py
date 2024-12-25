import time
from uuid import uuid4
from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.customers.entities import CustomerEntity
from core.apps.questions.models.questions import Test


class Customer(TimedBaseModel):
    def get_expires_in():
        return int(time.time()) + 3600

    def get_refresh_expires_in():
        return int(time.time()) + 1209600

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
        default=get_expires_in,
    )

    refresh_expires_in = models.BigIntegerField(
        verbose_name='Время до истечения refresh token',
        default=get_refresh_expires_in,
    )

    picture = models.ImageField(
        verbose_name='Изображение профиля',
        upload_to='customers/pofile_pictures',
        blank=True,
        null=True,
    )

    in_process = models.BooleanField(
        verbose_name='В процессе прохождения теста',
        default=False,
    )

    role = models.CharField(
        verbose_name='Роль пользователя',
        max_length=50,
        choices=(
            ('CUSTOMER', 'Пользователь'),
            ('ADMIN', 'Администратор'),
        ),
        default='CUSTOMER',
    )

    def __str__(self) -> str:
        return self.email

    def to_entity(self) -> CustomerEntity:
        return CustomerEntity(
            id=self.id,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            picture=self.picture if self.picture else '',
            in_process=self.in_process,
            role=self.role,
            created_at=self.created_at,
        )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
