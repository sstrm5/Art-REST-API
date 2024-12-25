from dataclasses import dataclass
from datetime import datetime


@dataclass
class CustomerEntity:
    id: int
    email: str
    first_name: str
    last_name: str
    picture: str
    in_process: bool
    role: str
    created_at: datetime
