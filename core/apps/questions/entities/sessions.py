from dataclasses import dataclass


@dataclass
class Session:
    id: int
    user_id: int
    test_id: int
