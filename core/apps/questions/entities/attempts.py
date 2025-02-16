from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Iterable


@dataclass
class Attempt:
    id: int
    user_id: int
    test_id: int
    end_time: datetime
    time_spent: timedelta
    user_answers: dict[str, Iterable]
    total_score: int
    created_at: datetime
    updated_at: datetime
