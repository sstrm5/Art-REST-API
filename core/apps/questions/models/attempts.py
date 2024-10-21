from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.customers.models import Customer
from core.apps.questions.entities.attempts import Attempt as AttemptEntity
from core.apps.questions.models.questions import Test


class Attempt(TimedBaseModel):
    user = models.ForeignKey(
        Customer,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )

    test = models.ForeignKey(
        Test,
        verbose_name='Тест',
        on_delete=models.CASCADE,
    )

    start_time = models.DateTimeField(
        verbose_name='Начало выполнения теста',
    )

    end_time = models.DateTimeField(
        verbose_name='Конец выполнения теста',
        null=True,
    )

    user_answers = models.JSONField(
        verbose_name='Ответы пользователя',
    )

    total_score = models.IntegerField(
        verbose_name='Баллы',
        null=True,
    )


    class Meta:
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'


    def to_entity(self) -> AttemptEntity:
        return AttemptEntity(
            id=self.id,
            user_id=self.user.pk,
            test_id=self.test.pk,
            start_time=self.start_time,
            end_time=self.end_time,
            user_answers=self.user_answers,
            total_score=self.total_score,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def __str__(self) -> str:
        return f'Попытка #{self.id} пользователя {self.user} для теста {self.test}'
