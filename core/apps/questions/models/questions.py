from django.db import models

from core.apps.common.models import TimedBaseModel

from core.apps.questions.entities.questions import Question as QuestionEntity

class Question(TimedBaseModel):
    class Subjects(models.TextChoices):
        RUSSIAN_ART = 'RU', 'Russian'

    title = models.CharField(
        verbose_name='Заголовок вопроса',
        max_length=255,
    )
    description = models.TextField(
        verbose_name='Описание вопроса',
    )
    subject = models.CharField(
        verbose_name='Заголовок вопроса',
        max_length=255,
        choices=Subjects.choices,
        default=Subjects.RUSSIAN_ART,
    )
    is_visible = models.BooleanField(
        verbose_name='Виден ли вопрос в списке',
        default=True,
    )

    def to_entity(self) -> QuestionEntity:
        return QuestionEntity(
            id=self.id,
            title=self.title,
            description=self.description,
            subject=self.subject,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def __str__(self) -> str:
        return self.title
        
    
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
