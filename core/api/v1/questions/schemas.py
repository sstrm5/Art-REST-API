from datetime import datetime

from pydantic import BaseModel

from core.apps.questions.entities.questions import Question as QuestionEntity


class QuestionSchema(BaseModel):
    id: int
    title: str
    description: str
    subject: str
    created_at: datetime
    updated_at: datetime | None = None

    @staticmethod
    def from_entity(entity: QuestionEntity) -> 'QuestionSchema':
        return QuestionSchema(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            subject=entity.subject,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
