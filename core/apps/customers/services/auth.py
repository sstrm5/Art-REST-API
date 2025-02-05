from abc import ABC, abstractmethod
from dataclasses import dataclass
from celery import shared_task
from core.apps.customers.services.codes import BaseCodeService
from core.apps.customers.services.customers import BaseCustomerService
from core.apps.customers.services.senders import BaseSenderService


@dataclass(eq=False)
class BaseAuthService(ABC):
    customer_service: BaseCustomerService
    codes_service: BaseCodeService
    sender_service: BaseSenderService

    @abstractmethod
    def send_code_to_create(self, email: str, first_name: str, last_name: str):
        ...

    @abstractmethod
    def send_code_to_get(self, email: str):
        ...

    @abstractmethod
    def confirm_and_create(self, email: str, code: str, first_name: str, last_name: str):
        ...

    @abstractmethod
    def confirm_and_get(self, email: str, code: str, first_name: str, last_name: str):
        ...


class AuthService(BaseAuthService):
    def send_code_to_create(self, email: str, first_name: str, last_name: str):
        code = self.codes_service.generate_code(email=email)
        self.sender_service.send_code(
            email=email, code=code, first_name=first_name)

    def send_code_to_get(self, email: str):
        customer = self.customer_service.get_by_email(email=email)
        if not customer:
            raise ValueError(f'No customer found with email: {email}')
        code = self.codes_service.generate_code(email=email)
        self.sender_service.send_code(
            email=email, code=code, first_name=customer.first_name)

    def confirm_and_create(self, email: str, code: str, first_name: str, last_name: str,
                           device_info: str):
        self.codes_service.validate_code(code=code, email=email)
        customer = self.customer_service.get_or_create(
            email=email, first_name=first_name, last_name=last_name)
        access_token, refresh_token, expires_in = self.customer_service.generate_token(
            customer=customer,
            device_info=device_info,
        )

        return access_token, refresh_token, expires_in

    def confirm_and_get(self, email: str, code: str, device_info: str):
        self.codes_service.validate_code(code=code, email=email)
        customer = self.customer_service.get_by_email(email=email)
        access_token, refresh_token, expires_in = self.customer_service.generate_token(
            customer=customer,
            device_info=device_info,
        )

        return access_token, refresh_token, expires_in
