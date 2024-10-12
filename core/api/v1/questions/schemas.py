from dataclasses import Field
from datetime import datetime
from typing import Generic, TypeVar
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

