from abc import ABC, abstractmethod
from datetime import datetime
import json
from typing import Iterable

from core.api.v1.questions.filters import TestFilters, QuestionFilters
from core.api.filters import PaginationIn
from core.api.v1.questions.schemas import TestSchemaIn
from core.apps.questions.entities.questions import Test, Question, AnswersIn
from core.apps.questions.models.questions import (
    Test as TestModel,
    Question as QuestionModel,
    Answer as AnswerModel,
    )
from core.apps.questions.models.subjects import Subject
from core.apps.questions.exceptions.questions import (
    SubjectException,
    QuestionException,
    CreateException,
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
        qs = TestModel.objects.filter(is_visible=True)[pagination.offset:pagination.offset + pagination.limit]
        return [test.to_entity() for test in qs]

    def get_test_count(self, filters: TestFilters) -> int:
        return TestModel.objects.filter(is_visible=True).count()
    
    def create_test(self, data: TestSchemaIn) -> Test:
        data = data.data
        test_data = data.test_info
        question_list_data = data.questions
        try:
            subject = test_data.subject
            subject, _ = Subject.objects.get_or_create(subject=subject)
        except:
            raise SubjectException()
        
        try:
            test = TestModel.objects.create(
                title=test_data.title,
                description=test_data.description,
                subject=subject,
                work_time=test_data.work_time,
                question_count=len(question_list_data),
                created_at=datetime.now(),
                updated_at=datetime.now(),
                is_visible=True,
            )
        except Exception:
            raise Exception
        
        try:
            for question_data in question_list_data:
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
                    answer = AnswerModel.objects.create(
                        text=answer_data,
                        is_correct=answers_dict[answer_data],
                        question=question,
                        created_at=datetime.now(),
                        updated_at=datetime.now(),
                    )
        except Exception:
            raise Exception
        return test.to_entity()
        

    def check_test(self, data: AnswersIn, questions: Iterable[Question]):
        correct_answers = {}
        for question_number, question in enumerate(questions, 1):
            correct_question_answers = []
            for answer_index, answer_is_correct in enumerate(question.answers.values()):
                if answer_is_correct:
                    correct_question_answers.append(answer_index)
            correct_answers[str(question_number)] = correct_question_answers
        
        user_answers = data.user_answers
        total_score = 0
        for question_number in range(1, len(user_answers) + 1):
            question_number = json.dumps(question_number)
            if user_answers[question_number] == correct_answers[question_number]:
                    total_score += 1

        return data.test_id, user_answers, correct_answers, total_score


class ORMQuestionService(BaseQuestionService):
    def get_question_list(self, test_id) -> Iterable[Question]:
        qs = QuestionModel.objects.filter(is_visible=True, test__id=test_id)
        return [question.to_entity() for question in qs]
    
    def get_question_count(self, test_id) -> int:
        return QuestionModel.objects.filter(is_visible=True, test_id=test_id).count()

    