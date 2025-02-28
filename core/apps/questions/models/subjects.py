from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.questions.entities.subjects import Subject as SubjectEntity


class Subject(TimedBaseModel):
    subject = models.CharField(
        verbose_name='Тема',
        max_length=255,
    )
    is_visible = models.BooleanField(
        verbose_name='Видна ли тема в списке',
        default=True,
    )

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

    def __str__(self) -> str:
        return self.subject

    def to_entity(self) -> SubjectEntity:
        return SubjectEntity(
            id=self.id,
            subject=self.subject,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
