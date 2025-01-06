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


@dataclass
class CustomerSession:
    id: int
    customer: CustomerEntity
    access_token: str
    refresh_token: str
    expires_in: int
    refresh_expires_in: int
    device_info: str
