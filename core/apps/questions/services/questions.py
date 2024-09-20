from abc import ABC, abstractmethod
from typing import Iterable

from core.api.v1.questions.filters import TestFilters, QuestionFilters
from core.api.filters import PaginationIn
from core.apps.questions.entities.questions import Test, Question
from core.apps.questions.models.questions import Test as TestModel, Question as QuestionModel

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
        qs = TestModel.objects.filter(is_visible=True)[pagination.offset:pagination.offset + pagination.limit]
        return [test.to_entity() for test in qs]

    def get_test_count(self, filters: TestFilters) -> int:
        return TestModel.objects.filter(is_visible=True).count()


class ORMQuestionService(BaseQuestionService):
    def get_question_list(self, test_id) -> Iterable[Question]:
        qs = QuestionModel.objects.filter(is_visible=True, test__id=test_id)
        return [question.to_entity() for question in qs]
    
    def get_question_count(self, test_id) -> int:
        return QuestionModel.objects.filter(is_visible=True, test_id=test_id).count()

    