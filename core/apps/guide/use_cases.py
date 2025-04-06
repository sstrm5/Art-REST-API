from dataclasses import dataclass

from core.apps.guide.services.guide import BaseCardService


@dataclass
class GetDetailInfoGuideCard:
    card_service: BaseCardService

    def execute(self, card_id: int) -> dict:
        card = self.card_service.get_card_by_id(card_id=card_id)
        return card


@dataclass
class SearchCardsUseCase:
    card_service: BaseCardService

    def execute(self, query):
        cards = self.card_service.search_cards(query=query)
        return cards
