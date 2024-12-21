from dataclasses import dataclass
import datetime


@dataclass
class CustomerEntity:
    id: int
    email: str
    first_name: str
    last_name: str
    picture: str
    completed_tests: list
    in_process: bool
    role: str
    created_at: datetime
