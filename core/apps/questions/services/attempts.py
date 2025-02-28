from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Iterable
from core.apps.customers.entities import CustomerEntity
from core.apps.customers.models import Customer as CustomerModel
from core.apps.questions.entities.attempts import Attempt as AttemptEntity
from core.apps.questions.exceptions.questions import AttemptDoesNotExistException, TestNotFoundException
from core.apps.questions.models.attempts import Attempt as AttemptModel
from core.apps.questions.models.questions import Test as TestModel
import json


class BaseAttemptService(ABC):
    @abstractmethod
    def create_attempt(
        self,
        customer: CustomerEntity,
        test_id: int,
    ) -> AttemptEntity:
        ...

    @abstractmethod
    def get_attempt_list(self, test_id: int) -> AttemptEntity:
        ...


class ORMAttemptService(BaseAttemptService):
    def create_attempt(
        self,
        customer: CustomerEntity,
        test_id: int,
    ) -> AttemptEntity:
        try:
            test = TestModel.objects.get(id=test_id)
        except:
            raise TestNotFoundException()

        customer = CustomerModel.objects.get(id=customer.id)

        # номер последней попытки = кол-во попыток пользователя пройти тест
        attempt_number = AttemptModel.objects.filter(
            user=customer, test=test).count()

        # проверка наличия попытки для этого пользователя и теста
        if attempt_number:
            attempt_number += 1
        else:
            attempt_number = 1

        # время начала и конца попытки
        current_time = datetime.now()
        end_time = current_time + timedelta(seconds=(test.work_time * 60))

        # создание "пустой" попытки в БД
        attempt = AttemptModel.objects.create(
            user=customer,
            test=test,
            end_time=end_time,
            user_answers={},
            total_score=0,
            attempt_number=attempt_number,
            created_at=current_time,
            updated_at=current_time,
        )

        return attempt.to_entity()

    def update_attempt(self, user_id: int, test_id: int, user_answers: dict[str, list[str]]):
        customer = CustomerModel.objects.get(id=user_id)
        test = TestModel.objects.get(id=test_id)
        # номер последней попытки = кол-во попыток пользователя пройти тест
        attempt_number = AttemptModel.objects.filter(
            user=customer, test=test).count()
        attempt = AttemptModel.objects.filter(
            user=customer,
            test=test,
            attempt_number=attempt_number).first()
        if not user_answers:
            return attempt.to_entity()
        attempt.user_answers = user_answers
        attempt.save()

        return attempt.to_entity()

    def get_attempt_list(self, test_id: int) -> list[AttemptEntity]:
        attempts = AttemptModel.objects.filter(test_id=test_id)
        return [attempt.to_entity() for attempt in attempts]

    def get_attempt_list_by_customer(
            self,
            test_id: int,
            token: str,
    ) -> list[AttemptEntity]:
        attempts = AttemptModel.objects.filter(
            test_id=test_id, user__access_token=token)
        return [attempt.to_entity() for attempt in attempts]

    def get_customer_attempt_list(self, user_id: int):
        attempts = AttemptModel.objects.filter(
            user__id=user_id).order_by('-end_time')
        return [attempt.to_entity() for attempt in attempts]

    def get_last_attempt(self, user_id: int):
        attempt = AttemptModel.objects.filter(
            user_id=user_id).order_by('-created_at').first()
        if not attempt:
            raise AttemptDoesNotExistException()
        return attempt.to_entity()

    def get_by_id(self, attempt_id: int):
        attempt = AttemptModel.objects.filter(id=attempt_id).first()
        if not attempt:
            raise AttemptDoesNotExistException()
        return attempt.to_entity()

    def update_end_time(
            self,
            user_id: int,
            end_time: datetime,
            time_spent: timedelta,
    ):
        attempt = AttemptModel.objects.filter(
            user_id=user_id).order_by('-created_at').first()
        if not attempt:
            raise AttemptDoesNotExistException()
        attempt.end_time = str(end_time)
        attempt.time_spent = str(time_spent)
        attempt.save()

    def fill_blank_answers(
            self,
            attempt_id: int,
            question_count: int,
    ):
        attempt = AttemptModel.objects.get(id=attempt_id)
        user_answers = attempt.user_answers
        for question_number in range(1, question_count + 1):
            question_number = str(question_number)
            if question_number not in user_answers.keys():
                user_answers[question_number] = []
        attempt.user_answers = user_answers
        attempt.save()
