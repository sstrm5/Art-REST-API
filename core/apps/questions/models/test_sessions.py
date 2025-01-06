from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.customers.models import Customer
from core.apps.questions.models.questions import Test
from core.apps.questions.entities.test_sessions import TestSession as TestSessionEntity


class TestSession(TimedBaseModel):
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

    class Meta:
        verbose_name = 'Сессия'
        verbose_name_plural = 'Сессии'

    def __str__(self):
        return f"Test-session #{self.id} - {self.user.first_name} {self.user.last_name} - {self.test.title}"

    def to_entity(self) -> TestSessionEntity:
        return TestSessionEntity(
            id=self.id,
            user_id=self.user.id,
            test_id=self.test.id,
        )
