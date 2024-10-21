from abc import ABC, abstractmethod
from datetime import datetime
from typing import Iterable

from core.apps.customers.models import Customer as CustomerModel
from core.apps.questions.entities.attempts import Attempt as AttemptEntity
from core.apps.questions.models.attempts import Attempt as AttemptModel
from core.apps.questions.models.questions import Test as TestModel


class BaseAttemptService(ABC):
    @abstractmethod
    def create_attempt(
        self,
        user_id: int,
        test_id: int,
        start_time: datetime,
        end_time: datetime,
        user_answers: dict[int, Iterable],
        total_score: int,
        ) -> None:
        ...

    @abstractmethod
    def get_attempt_list(self, test_id: int) -> AttemptEntity:
        ...


class ORMAttemptService(BaseAttemptService):
    def create_attempt(
        self,
        user_id: int,
        test_id: int,
        start_time: datetime,
        end_time: datetime,
        user_answers: dict[int, Iterable],
        total_score: int,
        ) -> AttemptEntity:
        customer = CustomerModel.objects.get(id=user_id)
        test = TestModel.objects.get(id=test_id)
        attempt = AttemptModel.objects.create(
            user=customer,
            test=test,
            start_time=start_time,
            end_time=end_time,
            user_answers=user_answers,
            total_score=total_score,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        return attempt.to_entity()

    def get_attempt_list(self, test_id: int) -> list[AttemptEntity]:
        attempts = AttemptModel.objects.filter(test_id=test_id)
        return [attempt.to_entity() for attempt in attempts]
