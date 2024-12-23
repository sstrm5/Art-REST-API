from dataclasses import dataclass

from core.api.v1.questions.schemas import QuestionDataSchemaIn
from core.apps.customers.entities import CustomerEntity
from core.apps.customers.services.customers import BaseCustomerService

from core.apps.questions.entities.attempts import Attempt as AttemptEntity
from core.apps.questions.exceptions.questions import TestAlreadyStartedException, WrongAccessTokenException
from core.apps.questions.services.attempts import BaseAttemptService
from core.apps.questions.services.questions import BaseQuestionService, BaseTestService


@dataclass
class CreateTestUseCase:
    test_service: BaseTestService
    customer_service: BaseCustomerService

    def execute(self,
                subject: str,
                title: str,
                description: str,
                work_time: int,
                questions: list[QuestionDataSchemaIn],
                token: str,
                file,
                ):
        customer = self.customer_service.get_by_token(token)
        if not customer or customer.role != 'ADMIN':
            raise WrongAccessTokenException("Invalid access token")

        file_path = self.test_service.add_picture_to_test(file=file)

        try:
            test = self.test_service.create_test(
                subject=subject,
                title=title,
                description=description,
                work_time=work_time,
                questions=questions,
                file_path=file_path,

            )
        except Exception as error:
            raise error
        return test


@dataclass
class GetTestUseCase:
    test_service: BaseTestService
    question_service: BaseQuestionService

    def execute(self, test_id: int):
        question_list = self.question_service.get_question_list(
            test_id=test_id)
        test_duration = self.test_service.get_test_duration(
            test_id=test_id)
        return question_list, test_duration


@dataclass
class CheckTestUseCase:
    customer_service: BaseCustomerService
    test_service: BaseTestService
    question_service: BaseQuestionService

    def execute(self, test_id: int, token: str):
        customer = self.customer_service.get_by_token(token)
        question_list = self.question_service.get_question_list(
            test_id=test_id)
        user_answers, correct_answers, total_score = self.test_service.check_test(
            customer=customer,
            test_id=test_id,
            question_list=question_list,
        )
        self.customer_service.change_status(
            customer=customer, in_process=False)
        return user_answers, correct_answers, total_score


@dataclass
class GetAttemptListUseCase:
    attempt_service: BaseAttemptService
    customer_service: BaseCustomerService

    def execute(self, test_id: int):
        attempt_list: list[AttemptEntity] = self.attempt_service.get_attempt_list(
            test_id=test_id)
        attempt_list_with_customer_name = []
        for attempt_entity in attempt_list:
            user_id = attempt_entity.user_id
            customer: CustomerEntity = self.customer_service.get_by_id(user_id)
            user_name = f"{customer.first_name} {customer.last_name}"
            attempt_list_with_customer_name.append((attempt_entity, user_name))
        return attempt_list_with_customer_name


@dataclass
class CreateAttemptUseCase:
    attempt_service: BaseAttemptService
    customer_service: BaseCustomerService

    def execute(self, test_id: int, token: str):
        customer = self.customer_service.get_by_token(token=token)
        if customer.in_process:
            raise TestAlreadyStartedException()
        attempt = self.attempt_service.create_attempt(
            customer=customer,
            test_id=test_id,
        )
        self.customer_service.change_status(customer=customer, in_process=True)
        return attempt


@dataclass
class GetSubjectsUseCase:
    test_service: BaseTestService

    def execute(self):
        subjects = self.test_service.get_subjects()
        return subjects
