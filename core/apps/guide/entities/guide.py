from dataclasses import dataclass


@dataclass
class Card:
    id: int
    title: str
    subject: str
    text: str
    picture: str
