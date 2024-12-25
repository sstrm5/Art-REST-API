from abc import ABC, abstractmethod
from datetime import datetime
import json
import os
from typing import Iterable
from core.apps.common.exceptions import ServiceException
from core.apps.customers.entities import CustomerEntity
from ninja.files import UploadedFile
from core.api.v1.questions.filters import TestFilters, QuestionFilters
from core.api.filters import PaginationIn
from core.api.v1.questions.schemas import QuestionDataSchemaIn, TestSchemaIn
from core.apps.customers.models import Customer as CustomerModel
from core.apps.questions.entities.questions import Test, Question
from core.apps.questions.models.attempts import Attempt as AttemptModel
from core.apps.questions.models.questions import (
    Test as TestModel,
    Question as QuestionModel,
    Answer as AnswerModel,
)
from core.apps.questions.models.subjects import Subject
from core.apps.questions.exceptions.questions import (
    SubjectException,
    TestNotFoundException,
    TestWasNotStartedException,
)


class BaseTestService(ABC):
    @abstractmethod
    def get_test_list(self, filters: QuestionFilters, pagination: PaginationIn) -> Iterable[Test]:
        ...

    @abstractmethod
    def get_test_count(self, filters: QuestionFilters) -> int:
        ...


class BaseQuestionService(ABC):
    @abstractmethod
    def get_question_list(self, test_id: int) -> Iterable[Question]:
        ...

    @abstractmethod
    def get_question_count(self, test_id) -> int:
        ...


class BaseAnswerService(ABC):
    @abstractmethod
    def get_answer_list(self, filters: QuestionFilters, pagination: PaginationIn) -> Iterable[Question]:
        ...

    @abstractmethod
    def get_answer_count(self, filters: QuestionFilters) -> int:
        ...


class ORMTestService(BaseTestService):
    def get_test_list(self, filters: TestFilters, pagination: PaginationIn) -> Iterable[Test]:
        qs = TestModel.objects.filter(is_visible=True)[
            pagination.offset:pagination.offset + pagination.limit]
        return [test.to_entity() for test in qs]

    def get_test_count(self, filters: TestFilters) -> int:
        return TestModel.objects.filter(is_visible=True).count()

    def create_test(
            self,
            subject: str,
            title: str,
            description: str,
            work_time: int,
            questions: list[QuestionDataSchemaIn],
            file_path: str,
    ) -> Test:
        try:
            subject, _ = Subject.objects.get_or_create(subject=subject)
        except:
            raise SubjectException()

        try:
            test = TestModel.objects.create(
                title=title,
                description=description,
                subject=subject,
                work_time=work_time,
                is_visible=True,
                picture=file_path,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
        except Exception:
            raise Exception

        try:
            for question_data in questions:
                question = QuestionModel.objects.create(
                    title=question_data.title,
                    description=question_data.description,
                    test=test,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    is_visible=True,
                )
                answers_dict = question_data.answers
                for answer_data in answers_dict:
                    AnswerModel.objects.create(
                        text=answer_data,
                        is_correct=answers_dict[answer_data],
                        question=question,
                        created_at=datetime.now(),
                        updated_at=datetime.now(),
                    )
        except Exception:
            raise Exception
        return test.to_entity()

    def check_test(
            self,
            customer: CustomerEntity,
            test_id: int,
            question_list: Iterable[Question],
    ):
        user = CustomerModel.objects.get(id=customer.id)
        test = TestModel.objects.get(id=test_id)
        attempt_number = AttemptModel.objects.filter(
            user=user, test=test).count()

        # Создание словаря с правильными ответами
        correct_answers = {}
        for question_number, question in enumerate(question_list, 1):
            correct_question_answers = []
            for answer_index, answer_is_correct in enumerate(question.answers_dict.values(), 1):
                if answer_is_correct:
                    correct_question_answers.append(str(answer_index))
            correct_answers[str(question_number)] = correct_question_answers

        # Проверка ответов пользователя на правильность и оценивание
        user_answers = AttemptModel.objects.get(
            test=test_id,
            user=user,
            attempt_number=attempt_number,
        ).user_answers
        total_score = 0
        for question_number in range(1, len(user_answers) + 1):
            question_number = json.dumps(question_number)
            if user_answers[question_number] == correct_answers[question_number]:
                total_score += 1

        AttemptModel.objects.filter(
            user=user,
            test=test,
            attempt_number=attempt_number).update(total_score=total_score)

        return user_answers, correct_answers, total_score

    def get_test_duration(self, test_id: int) -> int:
        try:
            test = TestModel.objects.get(id=test_id)
        except:
            raise TestNotFoundException()
        return test.work_time

    def add_picture_to_test(self, file: UploadedFile):
        if not os.path.exists("media/questions/tests_pictures/"):
            os.makedirs("media/questions/tests_pictures/")
        file_path = f'questions/tests_pictures/{file.name}'
        with open(f'media/' + file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
        return file_path

    def get_subjects(self):
        return [subject.to_entity() for subject in Subject.objects.filter(is_visible=True)]


class ORMQuestionService(BaseQuestionService):
    def get_question_list(self, test_id) -> Iterable[Question]:
        try:
            qs = QuestionModel.objects.filter(
                is_visible=True, test__id=test_id)
        except Exception:
            raise TestNotFoundException()
        return [question.to_entity() for question in qs]

    def get_question_count(self, test_id) -> int:
        return QuestionModel.objects.filter(is_visible=True, test_id=test_id).count()
