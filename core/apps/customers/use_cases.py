from dataclasses import dataclass

from ninja import UploadedFile

from core.apps.customers.services.customers import BaseCustomerService
from core.apps.questions.services.attempts import BaseAttemptService
from core.apps.questions.services.questions import BaseTestService


@dataclass
class GetInfoAboutUserUseCase:
    customer_service: BaseCustomerService
    attempt_service: BaseAttemptService
    test_service: BaseTestService

    def execute(
        self,
        token: str,
        device_info: str,
    ):
        customer = self.customer_service.get_by_token(token=token)
        name = f"{customer.first_name} {customer.last_name}"
        customer_attempts = self.attempt_service.get_customer_attempt_list(
            user_id=customer.id
        )

        for attempt in customer_attempts:
            test = self.test_service.get_by_id(test_id=attempt.test_id)
            attempt.test_title = test.title
            attempt.question_count = test.question_count

        return (
            customer.id,
            customer.picture,
            name,
            customer.email,
            customer.created_at,
            customer_attempts,
        )


@dataclass
class UpdateCustomerInfoUseCase:
    customer_service: BaseCustomerService

    def execute(
        self,
        token: str,
        first_name: str,
        last_name: str,
        image_file: UploadedFile,
    ):
        customer = self.customer_service.get_by_token(token=token)
        if image_file:
            avatar_path = self.customer_service.save_avatar(
                image_file=image_file,
                customer=customer,
            )
            self.customer_service.change_avatar(
                customer=customer,
                avatar_path=avatar_path,
            )
        if first_name or last_name:
            self.customer_service.change_name(
                customer=customer,
                first_name=first_name,
                last_name=last_name,
            )
        return customer
