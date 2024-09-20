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
    created_at: datetime
    updated_at: datetime

