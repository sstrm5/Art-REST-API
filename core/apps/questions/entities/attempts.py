from dataclasses import dataclass
from datetime import datetime
from typing import Iterable


@dataclass
class Attempt:
    id: int
    user_id: int
    test_id: int
    start_time: datetime
    end_time: datetime
    user_answers: dict[int, Iterable]
    total_score: int
    created_at: datetime
    updated_at: datetime
