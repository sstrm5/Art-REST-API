from dataclasses import dataclass

from core.api.v1.questions.schemas import QuestionDataSchemaIn
from core.apps.customers.entities import CustomerEntity
from core.apps.customers.services.customers import BaseCustomerService

from core.apps.questions.entities.attempts import Attempt as AttemptEntity
from core.apps.questions.exceptions.questions import TestSessionAlreadyExistsException, TestSessionDoesNotExistException, TestSessionNotOverException, WrongAccessTokenException, WrongTestException
from core.apps.questions.services.attempts import BaseAttemptService
from core.apps.questions.services.questions import BaseQuestionService, BaseTestService
from core.apps.questions.services.test_sessions import BaseTestSessionService
from core.apps.questions.tasks import auto_submit_test
from datetime import datetime, timedelta, timezone


@dataclass
class CreateTestUseCase:
    test_service: BaseTestService
    customer_service: BaseCustomerService

    def execute(
            self,
            subject: str,
            title: str,
            description: str,
            work_time: int,
            questions: list[QuestionDataSchemaIn],
            token: str,
            device_info: str,
            file,
    ):
        customer = self.customer_service.get_by_token(
            token=token,
            device_info=device_info,
        )
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
class EndAttemptUseCase:
    customer_service: BaseCustomerService
    test_service: BaseTestService
    question_service: BaseQuestionService
    test_session_service: BaseTestSessionService
    attempt_service: BaseAttemptService

    def execute(
            self,
            token: str,
            device_info: str,
    ):
        customer = self.customer_service.get_by_token(
            token=token,
            device_info=device_info,
        )

        if not self.test_session_service.is_session_exists(user_id=customer.id):
            raise TestSessionDoesNotExistException()

        test_id = self.test_session_service.find_out_the_current_test(
            user_id=customer.id)

        question_list = self.question_service.get_question_list(
            test_id=test_id)

        self.test_service.check_test(
            customer=customer,
            test_id=test_id,
            question_list=question_list,
        )

        current_attempt = self.attempt_service.get_last_attempt(
            user_id=customer.id)

        self.attempt_service.update_end_time(
            user_id=customer.id,
            end_time=datetime.now(timezone.utc),
            time_spent=datetime.now(
                timezone.utc) - current_attempt.created_at,
        )

        question_count = len(question_list)

        self.attempt_service.fill_blank_answers(
            attempt_id=current_attempt.id,
            question_count=question_count,
        )

        self.customer_service.change_status(
            customer=customer, in_process=False)
        self.test_session_service.delete_session_by_user(user_id=customer.id)

        return test_id


@dataclass
class GetLastAttemptResultUseCase:
    customer_service: BaseCustomerService
    question_service: BaseQuestionService
    attempt_service: BaseAttemptService
    test_session_service: BaseTestSessionService
    test_service: BaseTestService

    def execute(
            self,
            token: str,
            device_info: str,
    ):
        customer = self.customer_service.get_by_token(
            token=token,
            device_info=device_info,
        )

        if self.test_session_service.is_session_exists(user_id=customer.id):
            raise TestSessionNotOverException()

        attempt = self.attempt_service.get_last_attempt(user_id=customer.id)

        test_id, user_answers, total_score = attempt.test_id, attempt.user_answers, attempt.total_score

        question_list = self.question_service.get_question_list(
            test_id=test_id)

        correct_answers = self.test_service.get_correct_answers(
            test_id=test_id,
            question_list=question_list,
        )

        return test_id, question_list, correct_answers, user_answers, total_score


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
class GetAttemptListByCustomerUseCase:
    attempt_service: BaseAttemptService
    customer_service: BaseCustomerService

    def execute(self, test_id: int, token: str):
        attempt_list: list[AttemptEntity] = self.attempt_service.get_attempt_list_by_customer(
            test_id=test_id,
            token=token,
        )
        return attempt_list


@dataclass
class CreateAttemptUseCase:
    attempt_service: BaseAttemptService
    customer_service: BaseCustomerService
    test_session_service: BaseTestSessionService
    test_service: BaseTestService

    def execute(
            self,
            token: str,
            test_id: int,
            device_info: str,
    ):
        customer = self.customer_service.get_by_token(
            token=token,
            device_info=device_info,
        )
        if self.test_session_service.is_session_exists(user_id=customer.id):
            # raise TestAlreadyStartedException()
            attempt = self.attempt_service.get_last_attempt(
                user_id=customer.id)
            if attempt.test_id == test_id:
                return attempt
            raise TestSessionAlreadyExistsException()
        attempt = self.attempt_service.create_attempt(
            customer=customer,
            test_id=test_id,
        )
        self.test_session_service.create_session(
            user_id=customer.id, test_id=test_id)
        self.customer_service.change_status(customer=customer, in_process=True)

        # end_time = attempt.end_time
        test_duration = self.test_service.get_test_duration(test_id=test_id)

        # Отложенная celery задача
        auto_submit_test.apply_async(kwargs={
                                     "token": token, "device_info": device_info},
                                     eta=datetime.now(timezone.utc) + timedelta(minutes=test_duration))

        return attempt


@dataclass
class GetSubjectsUseCase:
    test_service: BaseTestService

    def execute(self):
        subjects = self.test_service.get_subjects()
        return subjects


@dataclass
class UpdateAttemptAnswersUseCase:
    customer_service: BaseCustomerService
    attempt_service: BaseAttemptService
    test_session_service: BaseTestSessionService

    def execute(
            self,
            user_answers: dict[str, list[str]],
            token: str,
            test_id: int,
            device_info: str,
    ):
        customer = self.customer_service.get_by_token(
            token=token,
            device_info=device_info,
        )

        if not self.test_session_service.is_session_exists(user_id=customer.id):
            raise TestSessionDoesNotExistException()

        cur_test_id = self.test_session_service.find_out_the_current_test(
            user_id=customer.id)

        if test_id != cur_test_id:
            raise WrongTestException()

        attempt = self.attempt_service.update_attempt(
            user_id=customer.id,
            test_id=test_id,
            user_answers=user_answers,
        )
        return attempt


@dataclass
class GetCurrentTestUseCase:
    test_session_service: BaseTestSessionService
    customer_service: BaseCustomerService

    def execute(
            self,
            token: str,
            device_info: str,
    ):
        customer = self.customer_service.get_by_token(
            token=token,
            device_info=device_info,
        )

        if not self.test_session_service.is_session_exists(user_id=customer.id):
            raise TestSessionDoesNotExistException()

        test_id = self.test_session_service.find_out_the_current_test(
            user_id=customer.id)
        return test_id


@dataclass
class GetAttemptInfoUseCase:
    attempt_service: BaseAttemptService
    customer_service: BaseCustomerService
    test_service: BaseTestService
    question_service: BaseQuestionService

    def execute(
            self,
            token: str,
            device_info: str,
            attempt_id: int,
    ):
        customer = self.customer_service.get_by_token(
            token=token,
            device_info=device_info,
        )
        attempt = self.attempt_service.get_by_id(attempt_id=attempt_id)

        if customer.id != attempt.user_id:
            raise WrongAccessTokenException()

        question_list = self.question_service.get_question_list(
            test_id=attempt.test_id)
        question_count = len(question_list)
        correct_answers = self.test_service.get_correct_answers(
            test_id=attempt.test_id,
            question_list=question_list,
        )
        attempt.question_list = question_list
        attempt.question_count = question_count
        attempt.correct_answers = correct_answers

        return attempt
