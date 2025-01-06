from dataclasses import dataclass

from core.apps.customers.services.customers import BaseCustomerService
from core.apps.questions.services.attempts import BaseAttemptService


@dataclass
class GetInfoAboutUserUseCase:
    customer_service: BaseCustomerService
    attempt_service: BaseAttemptService

    def execute(
            self,
            token: str,
            device_info: str,
    ):
        customer = self.customer_service.get_by_token(
            token=token,
            device_info=device_info,
        )
        name = f"{customer.first_name} {customer.last_name}"
        customer_attempts = self.attempt_service.get_customer_attempt_list(
            user_id=customer.id)
        return customer.id, customer.picture, name, customer.email, customer.created_at, customer_attempts
