from abc import ABC, abstractmethod

from core.apps.guide.entities.guide import Card as CardEntity
from core.apps.guide.exceptions import CardDoesNotExistException
from core.apps.guide.models import Card


class BaseCardService(ABC):
    @abstractmethod
    def get_all_cards(self) -> list[CardEntity]: ...
    @abstractmethod
    def get_cards_by_subject(self, subject_title: str) -> list[CardEntity]: ...


class CardService(BaseCardService):
    def get_all_cards(self) -> list[CardEntity]:
        cards = Card.objects.all()
        return [card.to_entity() for card in cards]

    def get_cards_by_subject(self, subject_title: str) -> list[CardEntity]:
        cards = Card.objects.filter(subject__title=subject_title)
        return [card.to_entity() for card in cards]

    def get_card_by_id(self, card_id: int):
        try:
            card = Card.objects.get(id=card_id)
        except:
            raise CardDoesNotExistException()
        return card.to_entity()
