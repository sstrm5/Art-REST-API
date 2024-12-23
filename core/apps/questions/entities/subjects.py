from dataclasses import dataclass
from datetime import datetime


@dataclass
class Subject:
    id: int
    subject: str
    created_at: datetime
    updated_at: datetime
