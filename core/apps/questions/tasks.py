from celery import shared_task
from django.utils.timezone import now
from core.apps.customers.services.customers import BaseCustomerService
from core.apps.questions.containers import get_container
from core.apps.questions.models.test_sessions import TestSession
from core.apps.questions.services.questions import BaseQuestionService, BaseTestService
from core.apps.questions.services.test_sessions import BaseTestSessionService


@shared_task
def auto_submit_test(token: str, device_info: str):
    container = get_container()
    from core.apps.questions.use_cases import EndAttemptUseCase
    use_case = EndAttemptUseCase(
        customer_service=container.resolve(BaseCustomerService),
        test_service=container.resolve(BaseTestService),
        question_service=container.resolve(BaseQuestionService),
        test_session_service=container.resolve(BaseTestSessionService),
    )
    use_case.execute(token=token, device_info=device_info)
