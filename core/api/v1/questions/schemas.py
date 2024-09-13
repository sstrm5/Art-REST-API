from dataclasses import Field
from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel

from core.apps.questions.entities.questions import (
                                                    Test as TestEntity,
                                                    Question as QuestionEntity,
                                                    Answer as AnswerEntity,
                                                    )


TTestItem = TypeVar("TTestItem")


class TestSchema(BaseModel):
    id: int
    title: str
    description: str
    # subject: TTestItem | dict
    work_time: int
    question_count: int
    created_at: datetime
    updated_at: datetime | None = None

    @staticmethod
    def from_entity(entity: TestEntity) -> 'TestSchema':
        return TestSchema(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            subject=entity.subject,
            work_time=entity.work_time,
            question_count=entity.question_count,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class QuestionSchema(BaseModel):
    id: int
    test: str
    title: str
    description: str
    subject: str
    created_at: datetime
    updated_at: datetime | None = None

    @staticmethod
    def from_entity(entity: QuestionEntity) -> 'QuestionSchema':
        return QuestionSchema(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            subject=entity.subject,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class AnswerSchema(BaseModel):
    id: int
    question_id: int
    answer_text: str
    is_correct: bool
    created_at: datetime
    updated_at: datetime | None = None

    @staticmethod
    def from_entity(entity: AnswerEntity) -> 'AnswerSchema':
        return AnswerSchema(
            id=entity.id,
            question_id=entity.question_id,
            answer_text=entity.answer_text,
            is_correct=entity.is_correct,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
