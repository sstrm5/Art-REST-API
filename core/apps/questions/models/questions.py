from django.db import models
from django import forms

from core.apps.common.models import TimedBaseModel
from core.apps.questions.entities.questions import Question as QuestionEntity, Test as TestEntity, Answer as AnswerEntity
from .subjects import Subject

class Test(TimedBaseModel):
    title = models.CharField(
        verbose_name='Название теста',
        max_length=255,
        blank=True,
    )
    work_time = models.IntegerField(
        verbose_name='Время выполнения (мин)',
        blank=True,
    )
    question_count = models.IntegerField(
        verbose_name='Количество вопросов в тесте',
    )
    description = models.TextField(
        verbose_name='Описание теста',
        blank=True,
    )
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.filter(is_visible=True),
        label='subject',
        widget=forms.Select,
    )
    is_visible = models.BooleanField(
        verbose_name='Виден ли тест в списке',
        default=True,
    )


    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def to_entity(self) -> TestEntity:
        return TestEntity(
            id=self.id,
            title=self.title,
            description=self.description,
            subject=self.subject,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
    
    def __str__(self) -> str:
        return self.title


class Question(TimedBaseModel):
    # class Subjects(models.TextChoices):
    #     RUSSIAN_ART = 'RU', 'Russian'

    test = models.ForeignKey(
        Test,
        verbose_name='Тест',
        on_delete=models.CASCADE,
        blank=True
    )
    title = models.CharField(
        verbose_name='Заголовок вопроса',
        max_length=255,
    )
    description = models.TextField(
        verbose_name='Описание вопроса',
    )
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.filter(is_visible=True),
        label='subject',
        widget=forms.Select,
        blank=True,
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


class Answer(TimedBaseModel):
    question = models.ForeignKey(
        Question,
        verbose_name='Вопрос',
        on_delete=models.CASCADE,
    )
    text = models.CharField(
        verbose_name='Ответ',
        max_length=255,
    )
    is_correct = models.BooleanField(
        verbose_name='Правильный ли ответ',
        default=False,
    )

    def to_entity(self) -> AnswerEntity:
        return AnswerEntity(
            id=self.id,
            title=self.title,
            description=self.description,
            subject=self.subject,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
    
    def __str__(self) -> str:
        return self.text
    
    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
