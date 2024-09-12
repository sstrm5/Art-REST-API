from dataclasses import dataclass
from datetime import datetime


@dataclass
class Question:
    id: int
    title: str
    description: str
    subject: str
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


@dataclass
class Answer:
    id: int
    question_id: int
    answer_text: str
    is_correct: bool
    created_at: datetime
    updated_at: datetime
