from dataclasses import dataclass

from core.apps.customers.services.customers import BaseCustomerService
from core.apps.questions.services.attempts import BaseAttemptService


@dataclass
class GetInfoAboutUserUseCase:
    customer_service: BaseCustomerService
    attempt_service: BaseAttemptService

    def execute(self, token: str):
        customer = self.customer_service.get_by_token(token=token)
        name = f"{customer.first_name} {customer.last_name}"
        customer_attempts = self.attempt_service.get_customer_attempt_list(
            user_id=customer.id)
        return name, customer.email, customer.created_at, customer_attempts
