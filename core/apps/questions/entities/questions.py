from dataclasses import dataclass
from datetime import datetime


@dataclass
class Question:
    id: int
    test_id: int
    title: str
    answers: dict[str, bool]  # dict of answer_text: is_correct pairs
    description: str
    subject: str
    weight: int
    picture: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Test:
    id: int
    title: str
    description: str
    subject: str
    work_time: int
    question_count: int
    picture: str
    created_at: datetime
    updated_at: datetime


@dataclass
class AnswersIn:
    test_id: int


@dataclass
class AnswersOut:
    test_id: int
    user_answers: dict[int, int]
    correct_answers: dict[int, list[int]]
    total_score: int
