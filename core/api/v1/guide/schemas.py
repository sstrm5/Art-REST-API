from ninja import Schema

from core.apps.guide.entities.guide import Card as CardEntity


class GuideSchema(Schema):
    title: str
    subject: str
    text: str
    picture: str

    def from_entity(entity: CardEntity) -> 'GuideSchema':
        return GuideSchema(
            title=entity.title,
            subject=entity.subject,
            text=entity.text,
            picture=entity.picture,
        )
