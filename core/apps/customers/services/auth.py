from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.apps.customers.services.codes import BaseCodeService
from core.apps.customers.services.customers import BaseCustomerService
from core.apps.customers.services.senders import BaseSenderService


@dataclass(eq=False)
class BaseAuthService(ABC):
    customer_service: BaseCustomerService
    codes_service: BaseCodeService
    sender_service: BaseSenderService

    @abstractmethod
    def authorize(self, phone: str):
        ...

    @abstractmethod
    def confirm(self, phone:str, code: str):
        ...


class AuthService(BaseAuthService):
    def authorize(self, phone: str):
        customer = self.customer_service.get_or_create(phone=phone)
        code = self.codes_service.generate_code(customer=customer)
        self.sender_service.send_code(customer=customer, code=code)

    
    def confirm(self, phone: str, code: str):
        customer = self.customer_service.get(phone=phone)
        self.codes_service.validate_code(code=code, customer=customer)
        access_token, refresh_token, expires_in = self.customer_service.generate_token(customer=customer)

        return access_token, refresh_token, expires_in