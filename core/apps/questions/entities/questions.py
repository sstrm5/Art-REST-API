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
