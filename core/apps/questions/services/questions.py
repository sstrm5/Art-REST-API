from abc import ABC, abstractmethod
from typing import Iterable

from core.api.v1.questions.filters import QuestionFilters
from core.api.filters import PaginationIn
from core.apps.questions.entities.questions import Question
from core.apps.questions.models.questions import Question as QuestionModel

class BaseQuestionService(ABC):
    @abstractmethod
    def get_question_list(self, filters: QuestionFilters, pagination: PaginationIn) -> Iterable[Question]:
        ...

    @abstractmethod
    def get_question_count(self, filters: QuestionFilters) -> int:
        ...
    

class ORMQuestionService(BaseQuestionService):
    def get_question_list(self, filters: QuestionFilters, pagination: PaginationIn) -> Iterable[Question]:
        qs = QuestionModel.objects.filter(is_visible=True)[pagination.offset:pagination.offset + pagination.limit]
        return [question.to_entity() for question in qs]
    
    def get_question_count(self, filters: QuestionFilters) -> int:
        return QuestionModel.objects.filter(is_visible=True).count()
