from dataclasses import Field
from datetime import datetime
from typing import Generic, TypeVar
from core.apps.questions.entities.attempts import Attempt as AttemptEntity
from pydantic import BaseModel

from ninja import Schema

from core.apps.questions.entities.questions import (
                                                    Test as TestEntity,
                                                    Question as QuestionEntity,
                                                    )


TTestItem = TypeVar("TTestItem")
TData = TypeVar("TData")


class TestSchemaOut(Schema):
    id: int
    title: str
    description: str
    subject: TTestItem | dict
    work_time: int
    question_count: int
    created_at: datetime
    updated_at: datetime | None = None

    @staticmethod
    def from_entity(entity: TestEntity) -> 'TestSchemaOut':
        return TestSchemaOut(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            subject=entity.subject,
            work_time=entity.work_time,
            question_count=entity.question_count,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class QuestionSchemaOut(Schema):
    id: int
    test_id: int
    title: str
    answers: dict[str, bool]  # dict of answer_text: is_correct pairs
    description: str
    subject: str
    created_at: datetime
    updated_at: datetime | None = None

    @staticmethod
    def from_entity(entity: QuestionEntity) -> 'QuestionSchemaOut':
        return QuestionSchemaOut(
            id=entity.id,
            test_id=entity.test_id,
            title=entity.title,
            answers=entity.answers,
            description=entity.description,
            subject=entity.subject,
            weight=entity.weight,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class TestDataSchemaIn(Schema):
    id: int
    title: str
    description: str
    subject: str
    work_time: int
    question_count: int


class QuestionDataSchemaIn(Schema):
    id: int
    test_id: int
    title: str
    answers: dict[str, bool]  # dict of answer_text: is_correct pairs
    description: str
    subject: str


class TestAndQuestionDataSchemaIn(Schema):
    test_info: TestDataSchemaIn
    questions: list[QuestionDataSchemaIn]


class TestSchemaIn(Schema, Generic[TData]):
    data: TestAndQuestionDataSchemaIn


class AnswersSchemaIn(Schema):
    test_id: int
    user_answers: dict[str, list[int]]

class AnswersSchemaOut(Schema):
    test_id: int
    user_answers: dict[str, list[int]]
    correct_answers: dict[str, list[int]]
    total_score: int


class CheckUserExistenceIn(Schema):
    email: str


class CheckUserExistenceOut(Schema):
    is_user_exists: bool


class AttemptSchemaIn(Schema):
    user_id: int
    test_id: int
    start_time: datetime
    end_time: datetime
    user_answers: dict[str, list[int]]
    total_score: int


class AttemptSchemaOut(Schema):
    user_id: int
    test_id: int
    start_time: datetime
    end_time: datetime
    total_score: int

    def from_entity(entity: AttemptEntity) -> 'AttemptSchemaOut':
        return AttemptSchemaOut(
            user_id=entity.user_id,
            test_id=entity.test_id,
            start_time=entity.start_time,
            end_time=entity.end_time,
            total_score=entity.total_score,
        )
