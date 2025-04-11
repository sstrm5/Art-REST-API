from datetime import datetime, time
from typing import Generic, Optional, TypeVar
from core.apps.questions.entities.attempts import Attempt as AttemptEntity

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
    picture: str
    created_at: datetime
    updated_at: datetime | None = None

    @staticmethod
    def from_entity(entity: TestEntity) -> "TestSchemaOut":
        return TestSchemaOut(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            subject=entity.subject,
            work_time=entity.work_time,
            question_count=entity.question_count,
            picture=entity.picture,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class QuestionSchemaOut(Schema):
    id: int
    test_id: int
    title: str
    # dict of answer_index: answer_text pairs
    answers: list[dict[str, str]]
    description: str
    subject: str
    picture: str
    created_at: datetime
    updated_at: datetime | None = None

    @staticmethod
    def from_entity(entity: QuestionEntity) -> "QuestionSchemaOut":
        return QuestionSchemaOut(
            id=entity.id,
            test_id=entity.test_id,
            title=entity.title,
            answers=entity.answers,
            description=entity.description,
            subject=entity.subject,
            weight=entity.weight,
            picture=entity.picture,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class TestDataSchemaIn(Schema):
    title: str
    description: str
    subject: str
    work_time: int


class QuestionDataSchemaIn(Schema):
    title: str
    answers: dict[str, bool]  # dict of answer_text: is_correct pairs
    description: str
    subject: str


class TestAndQuestionDataSchemaIn(Schema):
    test_info: TestDataSchemaIn
    questions: list[QuestionDataSchemaIn]


class TestSchemaIn(Schema, Generic[TData]):
    data: TestAndQuestionDataSchemaIn


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
    test_id: int


class AttemptUpdateSchema(Schema):
    user_answers: dict[str, list[str]]
    test_id: int


class AttemptCustomerInfoSchema(Schema):
    attempt_id: int
    test_id: int
    test_title: str
    question_count: int
    total_score: int
    end_time: datetime
    time_spent: Optional[time]
    created_at: datetime

    def from_entity(entity: AttemptEntity) -> "AttemptCustomerInfoSchema":
        return AttemptCustomerInfoSchema(
            attempt_id=entity.id,
            test_id=entity.test_id,  # добавляю в customers.use_cases
            test_title=entity.test_title,  # добавляю в customers.use_cases
            question_count=entity.question_count,
            total_score=entity.total_score,
            end_time=entity.end_time,
            time_spent=entity.time_spent,
            created_at=entity.created_at,
        )


class AttemptSchemaOut(Schema):
    test_id: int
    user_answers: dict[str, list[str]]
    total_score: int
    created_at: datetime

    def from_entity(entity: AttemptEntity) -> "AttemptSchemaOut":
        return AttemptSchemaOut(
            id=entity.id,
            test_id=entity.test_id,
            end_time=entity.end_time,
            time_spent=entity.time_spent,
            user_answers=entity.user_answers,
            total_score=entity.total_score,
            created_at=entity.created_at,
        )


class AttemptSchemaOutWithName(Schema):
    attempt_info: AttemptSchemaOut
    user_name: str


class AnswersIn(Schema):
    test_id: int


class AnswersOut(Schema):
    test_id: int
    user_answers: dict[str, list[str]]
    correct_answers: dict[str, list[str]]
    question_list: list[QuestionSchemaOut]
    total_score: int


class CurrentTestIdSchema(Schema):
    test_id: int
    start_time: datetime
    duration: int


class LastAttemptResultSchema(Schema):
    test_id: int
    question_list: list[QuestionSchemaOut]
    correct_answers: dict[str, list[str]]
    user_answers: dict[str, list[str]]
    total_score: int


class AttemptInfoSchema(Schema):
    attempt_id: int
    test_id: int
    end_time: datetime
    time_spent: Optional[time]
    user_answers: dict[str, list[str]]
    total_score: int
    question_count: int
    question_list: list[QuestionSchemaOut]
    correct_answers: dict[str, list[str]]
    created_at: datetime

    def from_entity(entity: AttemptEntity) -> "AttemptInfoSchema":
        return AttemptInfoSchema(
            attempt_id=entity.id,
            test_id=entity.test_id,
            end_time=entity.end_time,
            time_spent=entity.time_spent,
            user_answers=entity.user_answers,
            total_score=entity.total_score,
            question_count=entity.question_count,
            question_list=[
                QuestionSchemaOut.from_entity(obj) for obj in entity.question_list
            ],
            correct_answers=entity.correct_answers,
            created_at=entity.created_at,
        )


class AttemptIDSchema(Schema):
    attempt_id: int
