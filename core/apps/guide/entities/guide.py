from dataclasses import dataclass


@dataclass
class Card:
    title: str
    subject: str
    text: str
    picture: str
