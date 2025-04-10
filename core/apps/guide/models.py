from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models

from core.apps.questions.models.subjects import Subject
from core.apps.common.models import TimedBaseModel
from core.apps.guide.entities.guide import Card as CardEntity

# Create your models here.


class Card(TimedBaseModel):
    title = models.CharField(
        verbose_name="Название карточки",
        max_length=255,
    )
    subject = models.ForeignKey(
        Subject,
        verbose_name="Тема",
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name="Текст карточки",
    )
    picture = models.ImageField(
        verbose_name="Изображение карточки",
        upload_to="cards",
        blank=True,
        null=True,
    )

    search_vector = SearchVectorField(null=True, blank=True)

    def to_entity(self) -> CardEntity:
        return CardEntity(
            id=self.pk,
            title=self.title,
            subject=self.subject.subject,
            text=self.text,
            picture=self.picture.url if self.picture else "",
        )

    def __str__(self) -> str:
        return self.title

    class Meta:
        indexes = [GinIndex(fields=["search_vector"])]

        verbose_name = "Карточка"
        verbose_name_plural = "Карточки"
