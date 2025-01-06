from dataclasses import dataclass


@dataclass
class TestSession:
    id: int
    user_id: int
    test_id: int
