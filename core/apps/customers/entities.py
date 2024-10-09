from dataclasses import dataclass
import datetime


@dataclass
class CustomerEntity:
    phone: str
    created_at: datetime
