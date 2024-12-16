from dataclasses import dataclass

from core.api.v1.questions.schemas import QuestionDataSchemaIn
from core.apps.questions.services.questions import BaseTestService


@dataclass
class CreateTestUseCase:
    test_service: BaseTestService

    def execute(self,
                subject: str,
                title: str,
                description: str,
                work_time: int,
                questions: list[QuestionDataSchemaIn],
                ):
        return self.test_service.create_test(
            subject=subject,
            title=title,
            description=description,
            work_time=work_time,
            questions=questions,
        )
